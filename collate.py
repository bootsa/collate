#!/usr/bin/env python3
'''
Collate
=======

A webpage combiner to take a list of webpages and combine them into one.

A learning project.

Originally using lxml with principles from:
* http://docs.python-guide.org/en/latest/scenarios/scrape/

Moved over to BeautifulSoup with:
* http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python

May implement Scrapy (http://doc.scrapy.org/en/latest/intro/tutorial.html) in the end...

May produce as a Django add on.

Basic breakdown:
* produce url and selector list
** embedded dictionary list (href, selectortype, selectorname)
** editable
** jquery highlighting selector selection?
* generate unique tokens from URLs for internal anchors/links, append to list
* retrieve each content
** append token to selector ID (remove styling?)
** add title and anchor link (within selector)
** append to cumulative store
* process cumulative store
** replace links with anchor names
* generate table of contents
* build collated page
** html header
** table of contents
** cumulative content
** html close
* turn into ebook?
** process with calibre?

'''

import requests
import bs4
import random
from urllib.parse import urljoin, urlparse


# a list of URLs to iterate through and combine in order
resources = [
	{'href':'http://localhost/testpages/testpage1.html', 'selectortype':'div', 'selectorname':'content'},
	{'href':'http://localhost/testpages/testpage2.html', 'selectortype':'div', 'selectorname':'content'}
	]

def genTokens(res):
	# TODO: Check for duplication (or create a better system)
	for r in res:
		token = str(random.randint(100000,1000000))
		# TODO: \/ this looks very ugly but seems to work
		pagename = str(r['href'].strip('/').rsplit('/',1)[-1].split(".html")[0])
		r['token'] = token
		r['pagename'] = pagename
		r['pagelink'] = pagename + "-" + token

def genTOC(res):
	toc = """
	<h1>Collated table of contents</h1>
	<ul>
	"""
	for r in res:
		toc += "<li><a href='#" + r['pagelink'] + "'>" + r['pagename'] + "</a></li>"
	toc += "</ul>"
	return toc

def getPagelink(ref,link):
	# get absolute path of the link
	targetlink = urljoin(ref,link)
	# split the pagename and anchor from link
	# could do with a urlparse but would have to recombine somehow maybe urlunsplit... targetlinksplit = urlparse(targetlink)
	try:
		targeturl, targetanchor = targetlink.split('#',1)
	except:
		targeturl, targetanchor = targetlink, None
	# lookup in resources and get resultant pagelink if applicable
	for r in resources:
		if r['href'] == targeturl:
			outputlink = str(r['pagelink'])
			print(outputlink)
			# if there is anchor add '-' followed by the anchor
			if targetanchor:
				outputlink += "-" + targetanchor
			print(outputlink)
			return outputlink

def getContents(res):
	# TODO: soup returns a list of selector types - assuming there's only one... what happens when their's more (generate token here?)
	print(res)
	response = requests.get(res['href'])
	soup = bs4.BeautifulSoup(response.text, "lxml")
	# container = soup.select(res['selectortype'] + '#' + res['selectorname'])
	container = soup.find(res['selectortype'], id=res['selectorname'])
	# add token to container ID to prevent duplication in collated page
	# container[0]['id'] += "-" + str(res['token'])
	container['id'] += "-" + str(res['token'])
	# loop through A tags to
	# * change anchors to include pagelink
	# * change links referring to other imported content (need to check absolute and relative links - expand all links to absolute paths?)
	# * add an external link symbol to links that connect to content outside the collated info
	# for a in container[0].find_all('a'):
	for a in container.find_all('a'):
		print(a)
		# need to check for attribute 'name' using a.attrs?
		if 'name' in a.attrs:
			# TODO: add pagelink (pagename + token) to name
			a.attrs['name'] = res['pagelink'] + "-" + a.attrs['name']
		if 'href' in a.attrs:
			internallink = getPagelink(res['href'],a['href'])
			if internallink:
				# TODO: change href to pagelink of linked to page
				a['href'] = "#" + internallink
				# print("Change href to pagelink of linked to page")
			else:
				# add external link symbol to end of a.text
				print("add external link symbol to end of a.text")

	# add an anchor heading to internally link from TOC and other content
	# TODO: include heading/formatting tag if specified
	heading = soup.new_tag("a")
	# using dot format to set NAME attribute of A tag causes problems as it changes the name of the tag (the A) instead of adding an NAME attribute - use dictionary format instead
	heading['name'] = res['pagelink']
	heading.string = soup.title.string
	# container[0].contents.insert(0,heading)
	container.contents.insert(0,heading)
	# return container[0]
	return container


# build output web page from template, toc and output snippet

if __name__ == '__main__':

	genTokens(resources)

	filename = "output/collated.html"

	outputfile = open(filename, 'w')

	outputfile.write("""
	<html>
	 <head>
	  <title>collated pages</title>
	 </head>
	 <body>
	  <div id="toc">
	 """)
	
	outputfile.write(genTOC(resources))
	outputfile.write("</div>")

	for res in resources:
		outputfile.write(str(getContents(res)))


	# for contpage in cont:
	# 	coll_str += str(contpage)

	outputfile.write("""
	 </body>
	</html>
	""")

	outputfile.close()

	# print(coll_str)

		# might do some checking for certain div's to stop unwanted tabs


		# strip links and insert anchors
		# add to output file (snippet)


		# print("="*4, " ", res, ": ", "="*4)
		# # print(cont[:40])
		# print("="*40)
