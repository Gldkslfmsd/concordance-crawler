#!/usr/bin/env python3

"""ConcordanceCrawler command-line application.

This is its main file, you can find here the main function (its entry
point).
"""

import sys
import six
import argparse
from sys import stdout
import logging
from traceback import format_exc

from ConcordanceCrawler.core.bazwords import *
from ConcordanceCrawler.app.output_formatter import *
from ConcordanceCrawler.app.logging_crawler import *
from ConcordanceCrawler.__init__ import __version__

def get_args():
	'''Setup command line arguments

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

	# TODO -- does it work for all version without encoding=?
	if six.PY3 and sys.version_info.minor>=4 and False:
		filetype = argparse.FileType('w', encoding='UTF-8')

	else:
		filetype = argparse.FileType('w')
	parser.add_argument("-o","--output",
		default=stdout,
		type=filetype,
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
		choices=["json"],# ,"xml"], # TODO: fix and allow xml
		help="output format (default %(default)s)"
		)

	parser.add_argument("-v","--verbosity",
		default=1,
		choices=[0,1,2,3],
		type=int,
		help="""Verbosity level. Every level contains also messages from higher
		levels. All this messages are printed to stderr.
		0 (DEBUG) -- logs all visiting urls before visit.
		1 (DETAILS) -- logs all crawled urls and number of found concordances.
		2 (STATUS) -- regurarly logs total number of visited pages, crawled
		concordances and errors.
		3 (ERROR) -- logs just errors and anything else.
		"""
		)


	args = vars(parser.parse_args())
	return args


def main():
	# setup command-line arguments and get them from user
	args = get_args()
	word = args["word"]
	number = args["n"]
	# here is output formatter
	of = create_formatter(
		format=args["format"],
		output_stream=args["output"]
		)
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

	log_level = ["DEBUG","DETAILS","STATUS","ERROR"][args['verbosity']]

	# setup logger and print welcome message
	setup_logger(log_level)
	logging.info("ConcordanceCrawler version {0} started, press Ctrl+C for \
	interrupt".format(
		__version__))

	# setup crawler
	lc = LoggingCrawler(word,bazgen)
	lc.max_per_page = max_per_page
	lc.page_limited = page_limited
	lc.total_concordances = number

	# generator that crawls exact number of concordances
	concordances = ( c for _,c in zip(range(number), lc.yield_concordances(word)) )

	# find concordances:
	try:
		for c in concordances:
			of.output(c)
	except KeyboardInterrupt:
		lc.log_state()
		logging.info("\n\nConcordanceCrawler aborted, you can try to find " +
		"its output in " + args["output"].name)
	finally:
		# close output stream
		of.close()

if __name__=="__main__":
	main()
