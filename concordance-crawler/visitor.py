#!/usr/bin/env python3

'''Visit given url and find there a concordance.'''

import requests
from bs4 import BeautifulSoup
import re


def get_visible_text(html):
	soup = BeautifulSoup(html,"lxml")
	text = soup.findAll(text=True)
	def visible(element):
			if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
					return False
			elif re.match('<!--.*-->', str(element)):
					return False
			return True

	visible_texts = "".join(filter(visible, text))
	return visible_texts


def visit(url, target):
	rawhtml = requests.get(url).text
	text = get_visible_text(rawhtml)

	# TODO: ... (three dots) get lost, but that would be too complicated

	# cut text to list: [ sentence, delimiter, sentence, delimiter, ... ]
	# e.g. [ "Hello", "!", " How are you", "?", "I'm fine", "." ]
	chunks = re.split("([\n\.\?\!])",text)
	
	# join sentence and its terminal mark
	# -> [ "Hello!", " How are you?", "I'm fine." ]
	sentences = [ x+y for x,y in zip(chunks[::2],chunks[1::2]) ]

	reg = re.compile(".*(\s|^)"+target+"(\s|$).*",flags=re.IGNORECASE)

	# concordances are sentences containing target word as a standalone word
	concordances = list(filter(reg.match, sentences))
	return concordances


if __name__ == "__main__":
	pairs = [("http://leapfroggroup.org/","group"),
		("http://www.thinkbabynames.com/meaning/1/Dominik","Dominik"),
		("https://hungryhouse.co.uk/indian-takeaway","takeaway"),
		("http://www.writeawriting.com/","write")]

	for url,target in pairs:
		print()
		print()
		print(url,target)
		print("==========================")
		con = visit(url,target)
		for i in con:
			# to better see ends of lines
			print(">>>",i,"<<<")
