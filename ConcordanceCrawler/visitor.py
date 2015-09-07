#!/usr/bin/env python3

'''Visit given url and find there a concordance.'''

from bs4 import BeautifulSoup
import re
import datetime

import ConcordanceCrawler.urlrequest as urlrequest

def get_visible_text(html):
	'''Gets raw html, returns its plain text (without marks) that is visible by
	humans.
	'''
	#Taken from here: http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
	soup = BeautifulSoup(html,"lxml")
	text = soup.findAll(text=True)
	def visible(element):
			if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
					return False
			if re.match('<!--.*-->', str(element)):
					return False
			return True

	visible_texts = "".join(filter(visible, text))
	return visible_texts


def visit(url, target):
	'''Visits a page on given url and extracts all sentences containing
	target word from visible text.

	Args:
		url
		target

	Returns:
		a list of sentences
	'''
	rawhtml = urlrequest.get_raw_html(url)
	text = get_visible_text(rawhtml)

	# NOTE: ... (three dots) get lost, but that would be too complicated

	# cut text to list: [ sentence, delimiter, sentence, delimiter, ... ]
	# e.g. [ "Hello", "!", " How are you", "?", "I'm fine", "." ]
	chunks = re.split("([\n\.\?\!])",text)
	
	# join sentence and its terminal mark
	# -> [ "Hello!", " How are you?", "I'm fine." ]
	sentences = [ x+y for x,y in zip(chunks[::2],chunks[1::2]) ]

	# concordances are sentences containing target word as a standalone word
	regex = re.compile(".*(\s|^)"+target+"(\s|$).*",flags=re.IGNORECASE)
	concordances = list(filter(regex.match, sentences))

	return concordances

def visit_links(links, target_word):
	'''Gets list of links, visits them and crawls concordances.
	
	Args:
		links -- list of dicts, where dict is a link and has at least key 'link'
		target_word

	Returns:
		list of concordances, where a concordance is a dict with keys:
			url, date, concordance (a sentence), keyword
	'''
	concordances = []
	for i in links:
		url = i['link']
		concs = visit(url,target_word)
		date = str(datetime.datetime.now())
		for j in concs:
			c = {
				'url':url,
				'date':date,
				'concordance':j,
				'keyword':target_word
			}
			concordances.append(c)

	return concordances





if __name__ == "__main__":
#	pairs = [("http://leapfroggroup.org/","group"),
#		("http://www.thinkbabynames.com/meaning/1/Dominik","Dominik"),
#		("https://hungryhouse.co.uk/indian-takeaway","takeaway"),
#		("http://www.writeawriting.com/","write")]

#	for url,target in pairs:
#		print()
#		print()
#		print(url,target)
#		print("==========================")
#		con = visit(url,target)
#		for i in con:
#			# to better see ends of lines
#			print(">>>"+i+"<<<")

	import requests
#	print(get_visible_text(requests.get("https://en.wikipedia.org/wiki/Viceroy_of_Liangguang").text))
	x = visit_links([{'link':'http://www.writeawriting.com/'}],"write")
	print(x)
