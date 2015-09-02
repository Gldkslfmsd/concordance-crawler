#!/usr/bin/env python3

"""ConcordanceCrawler command-line application"""

import argparse
from sys import stdout
from json import dumps
from dict2xml import dict2xml
import logging

from ConcordanceCrawler import *

def get_args():
	'''Sets command line arguments

	Returns: a dict with arguments and their values
	'''
	parser = argparse.ArgumentParser(description='Crawl concordances')

	parser.add_argument("word",
		type=str,
		help="a target word"
		)

	parser.add_argument("-n",
		default=10,
		type=int,
		help="number of concordances to be crawled (default %(default)s)"
		)

	parser.add_argument("-p",
		default=None,
		type=int,
		help="maximum number of concordances per page (default: unlimited)"
		)

	parser.add_argument("-o","--output",
		default=stdout,
		type=argparse.FileType('w', encoding='UTF-8'),
		help="output file (default stdout)"
		)

	parser.add_argument("-b","--bazword-generator",
		default="RANDOM",
		type=str,
		choices=["RANDOM","WIKI_ARTICLES","WIKI_TITLES","NUMBERS"],
		help="""type of bazword generator, you can choose RANDOM (random
		four-letter words), WIKI_ARTICLES (words from random articles from
		English Wikipedia), WIKI_TITLES (words from titles of random articles
		from English Wikipedia), NUMBERS (increasing numbers from 0)"""
		)

	parser.add_argument("-f","--format",
		default="json",
		type=str,
		choices=["json","xml"],
		help="output format (default %(default)s)"
		)

	args = vars(parser.parse_args())
	return args


class OutputFormater():
	def __init__(self, format, output_stream):
		self.output = output_stream
		if format=="json":
			self.to_output = self._output_as_json
		else:
			self.to_output = self._output_as_xml

	def _output_as_xml(self,concordance):
		'''prints one concordance to output'''
		result = dict2xml({'item':concordance},indent=" "*4,wrap="root") + "\n"
		self.output.write(result)

	def _output_as_json(self,concordance):
		result = dumps(concordance,indent=4)+"\n"
		self.output.write(result)

	def __del__(self):
		try:
			self.output.close()
		except ValueError: 
			pass
		

def main():
	args = get_args()
	word = args["word"]
	number = args["n"]
	output 	= OutputFormater(
		format=args["format"],
		output_stream=args["output"]
		).to_output
	baz = args["bazword_generator"]
	max_per_page = args["p"]
	page_limited = True if max_per_page else False
	if baz=="RANDOM":
		bazgen = RandomShortWords()
	elif baz=="WIKI_ARTICLES":
		bazgen = WikipediaRandomArticle()
	elif baz=="WIKI_TITLES":
		bazgen = WikipediaRandomArticleTitles()
	elif baz=="NUMBERS":
		bazgen = IncreasingNumbers()

	def yield_concordances(word):
		'''Generator crawling concordances'''
		while True:
			links = crawl_links(word,1,bazgen)
			print("page with links crawled")
			for l in links:
#				l['link']='https://www.diffchecker.com/'
				#print("link:",l['link'])
				try:
					concordances = visit_links([l],word)
				except requests.exceptions.RequestException as e:
					print("some error occured",e)
					continue
				print("page visited, n concordances found")
				for i,c in enumerate(concordances):
					if page_limited and i>max_per_page:
						break
					res = { "bing_link": l, "concordance": c }
					yield res

# get exact number of concordances
	concordances = ( c for _,c in zip(range(number), yield_concordances(word)) )

	try:
		for c in concordances:
			output(c)
	except KeyboardInterrupt:
		print("aborted")

if __name__=="__main__":
	main()
