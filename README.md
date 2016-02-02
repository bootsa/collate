# collate
A simple python script to collate a series of webpages into a single page with internal linking.

A webpage combiner to take a list of webpages and combine them into one.

A learning project so unlikely to be beautiful or the best way of doing it...

Originally using lxml with principles from:
* http://docs.python-guide.org/en/latest/scenarios/scrape/

Moved over to BeautifulSoup with:
* http://blog.miguelgrinberg.com/post/easy-web-scraping-with-python

May implement Scrapy (http://doc.scrapy.org/en/latest/intro/tutorial.html) in the end...

May produce as a Django add on.

Basic breakdown:
* produce url and selector list
  * embedded dictionary list (href, selectortype, selectorname)
  * editable
  * jquery highlighting selector selection?
* generate unique tokens from URLs for internal anchors/links, append to list
* retrieve each content
  * append token to selector ID (remove styling?)
  * add title and anchor link (within selector)
  * append to cumulative store
* process cumulative store
  * replace links with anchor names
* generate table of contents
* build collated page
  * html header
  * table of contents
  * cumulative content
  * html close
* turn into ebook?
  * process with calibre?

