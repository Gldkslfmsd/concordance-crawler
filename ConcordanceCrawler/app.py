#!/usr/bin/env python3

"""ConcordanceCrawler command-line application"""

import argparse
from sys import stdout
from json import dumps
from dict2xml import dict2xml
import logging

from ConcordanceCrawler import *


DETAILS = logging.INFO-5
STATUS = logging.INFO

def log_details(*a):
 logging.log(DETAILS, *a)


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

	parser.add_argument("-v","--verbosity",
		default="STATUS",
		choices=["DEBUG","DETAILS","STATUS","ERROR"],
		help="""Verbosity level. Every level contains also messages from higher
		levels. All this messages are printed to stderr.
		DEBUG -- logs all visiting urls before visit.
		DETAILS -- logs just number of found concordances and errors.
		STATUS -- regurarly logs number of visited pages, crawled
		concordances and errors.
		ERROR -- logs errors (e.g. invalid urls and ssl certificates).
		"""
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

class LoggingCrawler():	
	'''Crawls concordances and logs statistics'''
	num_serps = 0 # number of serp (search engine result pages) downloaded
	serp_errors = 0
	num_pages = 0 # number of visited pages
	page_errors = 0 # number of errors during visiting pages
	num_concordances = 0 # number of found concordances

	def __init__(self, word, bazgen):
		self.word = word
		self.bazgen = bazgen

	def log_state(self):
		logging.info("""Crawling status 
	serp\t\t{num_serps} ({serp_errors} errors) 
	pages visited\t{num_pages} ({page_errors} errors)
	concordances\t{num_concordances}""".format(
			num_serps=self.num_serps,
			serp_errors=self.serp_errors,
			num_pages=self.num_pages,
			page_errors=self.page_errors,
			num_concordances=self.num_concordances))
#		self.brief_log_state()

#	def brief_log_state(self):
#		logging.info(
#			("Successfully crawled {num_concordances} concordances from {total_concordances} "+
#			"({percent}%)").format(
#			num_concordances=self.num_concordances,
#			total_concordances = self.total_concordances,
#			percent = self.num_concordances/self.total_concordances*100))

	def yield_concordances(self,word):
		'''Generator crawling concordances'''
		for link in self.yield_links():
			for con in self.yield_concordances_from_link(link):
				self.log_state()
				yield con

	def yield_links(self):
		while True:
			try:
				links = crawl_links(self.word,1,self.bazgen)
				self.num_serps += 1
			except requests.exceptions.RequestException as e:
				self.serp_errors += 1
				logging.error("\'{}\' occured".format(e))
				self.log_state()
				continue
			log_details("crawled SERP {}, parsed {} links".format(
				get_keyword_url(links[0]['keyword']), len(links)))
			for l in links:
				yield l

	def yield_concordances_from_link(self,l):
		#l['link']='https://www.diffchecker.com/'
		#print("link:",l['link'])
		try:
			logging.debug("trying to download {}".format(l['link']))
			concordances = visit_links([l],self.word)
			log_details("page {} visited, {} concordances found".format(
				l['link'],len(concordances)))
			self.num_pages += 1
		except requests.exceptions.RequestException as e:
			logging.error("\'{}\' occured during getting {}".format(
				e,l['link']))
			self.page_errors += 1
		else:
			for i,c in enumerate(concordances):
				# maximum limit of concordances per page reached
				if self.page_limited and i>self.max_per_page:
					break
				res = { "bing_link": l, "concordance": c }
				self.num_concordances += 1
				yield res



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

	log_level = args['verbosity']

	# shut down the logger from requests module
	logging.getLogger("requests").setLevel(logging.WARNING)
	# setup this logger:
	logging.addLevelName(DETAILS,"DETAILS")
	logging.addLevelName(STATUS,"STATUS")
	logging.basicConfig(level=log_level,
		format="%(asctime)-15s %(levelname)s: %(message)s")
	logging.getLogger("requests").setLevel(logging.WARNING)
	logging.info("ConcordanceCrawler started, press Ctrl+C for interrupt")

	lc = LoggingCrawler(word,bazgen)
	lc.max_per_page = max_per_page
	lc.page_limited = page_limited
	lc.total_concordances = number

	concordances = ( c for _,c in zip(range(number), lc.yield_concordances(word)) )

	try:
		for c in concordances:
			output(c)
	except KeyboardInterrupt:
		logging.info("\n\nConcordanceCrawler aborted, you can try to find " +
		"its output in " + args["output"].name)

if __name__=="__main__":
	main()
