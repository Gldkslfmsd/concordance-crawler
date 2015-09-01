#!/usr/bin/env python3

"""ConcordanceCrawler command-line application"""

import argparse
from sys import stdout

from ConcordanceCrawler import *

def get_args():
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
		from English Wikipedia), NUMBERS (increasing numbers from 1)"""
		)

	parser.add_argument("-f","--format",
		default="json",
		type=str,
		choices=["json","xml"],
		help="output format (default %(default)s)"
		)

	args = vars(parser.parse_args())
	return args

def main():
	args = get_args()
	word = args["word"]
	number = args["n"]
	output = args["output"]
	baz = args["bazword_generator"]
	if baz=="RANDOM":
		bazgen = RandomShortWords()
	elif baz=="WIKI_ARTICLES":
		bazgen = WikipediaRandomArticle()
	elif baz=="WIKI_TITLES":
		bazgen = WikipediaRandomArticleTitles()
	elif baz=="NUMBERS":
		bazgen = IncreasingNumbers()

	def yield_concordances(word):
		while True:
			links = crawl_links(word,1,bazgen)
			for l in links:
				concordances = visit_links([l],word)
				for c in concordances:
					res = { "bing_link": l, "concordance": c }
					yield res

# get exact number of concordances
	concordances = [ c for _,c in zip(range(number), yield_concordances(word)) ]

	def output_as_xml():
		import dict2xml
		result = dict2xml.dict2xml({'item':concordances},indent=" "*4,wrap="root") + "\n"
		output.write(result)

	def output_as_json():
		import json
		result = json.dumps(concordances,indent=4)+"\n"
		output.write(result)

	if args["format"] == "json":
		output_as_json()
	else:
		output_as_xml()

	output.close()
