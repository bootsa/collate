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

# a list of URLs to iterate through and combine in order
resources = [
	{'href':'http://localhost/testpage1.html', 'selectortype':'div', 'selectorname':'content'},
	{'href':'http://localhost/testpage2.html', 'selectortype':'div', 'selectorname':'content'}
	]

def getContents(res):
		response = requests.get(res['href'])
		pagename = res['href'].split('/')[-3:-1]
		soup = bs4.BeautifulSoup(response.text, "lxml")

		result = soup.select(res['selectortype'] + '#' + res['selectorname'])
		
		return result


# build output web page from template, toc and output snippet

if __name__ == '__main__':
	for res in resources:
		cont = getContents(res)

		# might do some checking for certain div's to stop unwanted tabs


		# strip links and insert anchors
		# add to output file (snippet)


		print("="*4, " ", res, ": ", "="*4)
		# print(cont[:40])
		print("="*40)
