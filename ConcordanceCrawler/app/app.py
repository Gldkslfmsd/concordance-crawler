#!/usr/bin/env python3

"""ConcordanceCrawler command-line application.

This is its main file, you can find here the main function (its entry
point).
"""

import sys
import six
if six.PY2:
	range = xrange
import argparse
from sys import stdout
import logging
from traceback import format_exc

from ConcordanceCrawler.core.bazwords import *
from ConcordanceCrawler.core.encoding import norm_encoding
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
		nargs="+",
		help="""A target word to be crawled. You can specify more of its forms
		(e.g. differing only by singular/plural, case, tense etc.). The first
		one will be considered as canonical form."""
		)

	parser.add_argument("-n", "--number-of-concordances",
		default=10,
		type=int,
		help="number of concordances to be crawled (default %(default)s)"
		)

	parser.add_argument("-m", "--max-per-page",
		default=None,
		type=int,
		help="maximum number of concordances per page (default: unlimited)"
		)

	parser.add_argument("--disable-english-filter",
		default=None,
		const=True,
		action='store_const',
		help="disable filtering Non-English sentences from concordances",
		)


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
		choices=["json","xml"],
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
		2 (STATUS) -- regularly logs total number of visited pages, crawled
		concordances and errors.
		3 (ERROR) -- logs just errors and anything else.
		"""
		)

	parser.add_argument("-p", "--part-of-speech",
		default=None,
		type=str,
		choices=["v","a","n","x"],
		help="""Target word's part-of-speech. Concordances with any forms of
		target word conjugated/inflected as given part-of-speech will be
		crawled. Options are v: verbs, a: adjectives, n: nouns, x: any other
		indeclinable part of speech (default).
		
		If your option is v, a or n, ConcordanceCrawler will terminate, unless you 
		installed `textblob` library first.

		Size of this library is not neglible, because it uses `nltk`, therefore
		it's not an integral part of ConcordanceCrawler. Install it manually
		with `pip install textblob`, if you wish. 

		Instead of it you can also omit this option, decline your target word
		manually and use all its forms as additional values for `word`
		argument.

		If you have installed textblob and you choose v, a or n, its automatic
		lemmatizing of English will be used and other arguments for `word` than
		the first one will be ignored.
		"""
		)

	parser.add_argument("-e", "--encoding",
		default=None,
		type=str,
		help="""Select filtering of document by encoding. This option impacts
		quality of resulting corpus. If not given, documents without respect to
		their encoding will be crawled. If you select ASCII, all concordances
		containing any non-ASCII character will be removed. If you select any other
		charset, all documents without this charset specification in http header or in html
		metatag will be ignored (as well as documents with unequal charset
		value in http header and in metatag).
		"""
		)


	args = vars(parser.parse_args())
	return args

def use_textblob_lemmatizer(lc, pos):
	try:
		from ConcordanceCrawler.core.lemmatizer_concordance_filter import lemmatizing_concordance_filtering
	except ImportError as e:
		print(e)
		import sys
		sys.exit("""You have --part-of-speech among your options, your intention
is to use automatic lemmatizing of verbs, adjectives or nouns, but you
don't have `textblob` library installed. ConcordanceCrawler will terminate.

Please install textblob by using `pip install textblob`.

Or you can omit --part-of-speech option, conjugate/inflect your target word
by yourself and use it as additional argument for word. See help message
for more info.""")
	else:
		lc.setup(concordance_filtering=
			lambda sentence, target:
				lemmatizing_concordance_filtering(sentence, target, pos)
				)

def config_encoding(lc, enc):
	if enc is None:
		lc.setup(norm_encoding=lambda s, h: s)
	elif enc.lower()=="ascii":
		def ascii_filter(sentence):
			return all(ord(c) < 128 for c in sentence)
		lc.setup(norm_encoding=lambda s, h: s, 
			sentence_filter=ascii_filter)
	else:
		if enc.lower() not in ["utf-8", "utf-16", "utf-32", "iso-8859-1", "iso-8859-2",
			"gb2312", "gb18030"]:
			lc.Logger.warning("Are you sure you want to crawl only documents with {0}"
			" charset? It doesn't seem like any common valid encoding name. Maybe"
			" there aren't any documents in {0} charset on the Internet, so you will never get any"
			" concordances. But it's your option.".format(enc))

		lc.setup(norm_encoding=
			lambda doc, head: norm_encoding(doc, head, allowed=enc)
			)

			



def main():

	args = get_args()
	# setup command-line arguments and get them from user
	words = args["word"]
	number = args["number_of_concordances"]
	baz = args["bazword_generator"]
	max_per_page = args["max_per_page"]
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


	lc = LoggingCrawler(words,bazgen)

	pos = args['part_of_speech']
	if pos is None or ( len(pos)==1 and pos[0] == 'x' ):
		pass
	else:
		use_textblob_lemmatizer(lc, pos)

	# setup logger
	setup_logger(log_level)

	# here is output formatter
	of = create_formatter(
		format=args["format"],
		output_stream=args["output"]
		)

	# setup crawler
	lc.max_per_page = max_per_page
	lc.page_limited = page_limited
	#lc.total_concordances = number
	lc.Logger.setLevel(log_level)

	if args['disable_english_filter']:
		lc.setup(language_filter=lambda _: True)

	config_encoding(lc, args['encoding'])

	logging.info("ConcordanceCrawler version {0} started, press Ctrl+C for \
	interrupt".format(
		__version__))

	# generator that crawls exact number of concordances
	concordances = lc.yield_concordances(words)
	# find concordances:
	try:
		i = 0
		for c in concordances:
			of.output(c)
			i += 1
			if i>= number:
				break
	except KeyboardInterrupt:
		lc.log_state()
		logging.info("\n\nConcordanceCrawler aborted, you can try to find " +
		"its output in " + args["output"].name)
	finally:
		# close output stream
		of.close()

if __name__=="__main__":
	main()
