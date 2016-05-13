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
import re

from ConcordanceCrawler.core.bazwords import *
from ConcordanceCrawler.core.encoding import norm_encoding
from ConcordanceCrawler.app.output_formatter import *
from ConcordanceCrawler.core.logging_crawler import *
from ConcordanceCrawler.app.load_from_corpus import load_from_corpus
from ConcordanceCrawler.__init__ import __version__

def get_args():
	'''Setup command line arguments

	Returns: a dict with arguments and their values
	'''
	parser = argparse.ArgumentParser(description='''Select a word. ConcordanceCrawler
	enables you to download from the Internet any number of English sentences
	containing the word selected by you! 

	You can start a very new crawling job (then don't forget to include at
	least the `word` option) or you can continue with a job that was
	unexpectedly interrupted earlier, then you must include options
	`--backup-file BACKUP_FILE`, `--extend-corpus EXTEND_CORPUS` and
	`--continue-from-backup CONTINUE_FROM_BACKUP`.
	''')

	parser.add_argument("word",
		type=str,
		nargs="*",
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
		default=".*",
		type=str,
		help="""Target word's part-of-speech tag regex. As concordances will be
		crawled only sentences containing
		target word in forms whose part-of-speech tag matches regex specified
		by this option. 


		Tag values are adopted from Penn Treebank II tagset, see
		http://www.clips.ua.ac.be/pages/mbsp-tags for detailed description.

		Example: assume that target word is "fly" and given regex is
		"V.*", it means we want to crawl only verbs. Then a word "flies" (tagged
		"VBS") matches, as well as "flew" whose tag is "VBD". On the other hand
		an insect "fly" with tag "NN" doesn't match, so sentences with this word
		will be ignored. 

	
		Default value for this option is ".*", it means any
		arbitrary part-of-speech. If you select other regex (e.g. "V.*" for
		verbs, "N.*" for nouns, "J.*" for adjectives), then a `textblob` library
		will be used.

		Size of this library is not neglible, because it uses `nltk`, therefore
		it's not an integral part of ConcordanceCrawler. You must install it manually
		with `pip install textblob` and `python -m textblob.download_corpora`,
		if you wish. 

		Instead of it you can also omit this option, decline your target word
		manually and use all its forms as additional values for `word`
		argument.
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

	#########################################
	# backup options:

	parser.add_argument("--backup-off",
		default=None,
		const=True,
		action='store_const',
		help="""Don't create crawling status backup file. A corpus cannot be
		extended in future, even if crawling will be unexpectedly aborted."""
		)

	parser.add_argument("--backup-file",
		default="ConcordanceCrawler.backup",
		type=str,
		help="""Name for backup file. This backup file allows you to continue
		aborted crawling job and extend corpus. Default name is
		`ConcordanceCrawler.backup`."""
		)

	parser.add_argument("--extend-corpus",
		default=None,
		type=argparse.FileType("a"),
		help="""A corpus created in previous crawling job which will be
		extended now."""
		)

	parser.add_argument("--continue-from-backup",
		default=None,
		type=argparse.FileType("r"),
		help="""Continue crawling job from this backup file."""
		)

	
	def nonnegative(string):
		msg = "%r must be a nonnegative integer" % string
		try:
			N = int(string)
			if N<0:
				raise argparse.ArgumentTypeError(msg)
		except ValueError:
			raise argparse.ArgumentTypeError(msg)
		return N

	parser.add_argument("--buffer-size",
		default=10**6,
		type=nonnegative,
		help="""Setup maximal number of items in memory buffers which are used
		to prevent repeated visit of the same url and repeated crawling of
		the same concordance. 
		Default value is 1000000. Selecting of too big
		number can lead to out of memory error (but this should happen only
		after a very long time). Selecting of small number can lead to repeated
		visit of same url or repeated crawling of the same concordance, because
		the buffers are like queues, when they are full they delete the old values
		to save the new ones.
		"""
		)

	args = vars(parser.parse_args())

	#############################
	# constraints:
	ext_cont = [args['extend_corpus'], args['continue_from_backup']].count(None)
	if ext_cont == 1:
		parser.print_usage()
		sys.exit("If you want to extend corpus, you must to input both "
		"options --extend-corpus and --continue-from-backup."
		)
	if (args['word'] == [] and ext_cont==2) or (ext_cont==0 and args['word']!=[]):
		parser.print_usage()
		sys.exit("\nYou can either download a brand new corpus, then input at \n"
		"least the `word` option and omit options `--extend-corpus` and\n"
		"`--continue-from-backup`. Or you can continue crawling job from backup,\n"
		"then input options `--continue-from-backup` and `--extend-corpus` and\n"
		"omit `word` option.\n"
		"\nSee ConcordanceCrawler -h for more info.")

	return args, "backup" if ext_cont==0 else "run"

def use_textblob_lemmatizer(lc, pos):

	# in this case a simple_condordance_filter.py is used
	if pos == ".*":
		return

	# otherwise lemmatizer_concordance_filter.py is used
	try:
		pos_regex = re.compile(pos)
	except re.error as e:
		sys.exit(str(e)+"\n\nError occured during compiling part-of-speech tag \n"
		"regex. Please ensure it's a corect regular expression.")
	

	try:
		from ConcordanceCrawler.core.lemmatizer_concordance_filter import lemmatizing_concordance_filtering
	except ImportError as e:
		print(e)
		#import sys
		sys.exit("""You have --part-of-speech among your options, your intention
is to use automatic lemmatizing, but you don't have `textblob` library
installed. ConcordanceCrawler will terminate.

Please install textblob by using `pip install textblob` and `python -m
textblob.download_corpora`.

Or you can omit --part-of-speech option, conjugate/inflect your target word
by yourself and use it as additional argument for word. See help message
for more info.""")



	lc.setup(concordance_filtering=
		lambda sentence, target:
			lemmatizing_concordance_filtering(sentence, target, pos_regex)
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

def save_backup(args):
	if args['backup_off'] is not None:
		return
	bf = open(args['backup_file'], "w")
	bf.write("# ConcordanceCrawler-"+__version__+"\n")
	from time import ctime
	bf.write("# "+ctime()+"\n")
	import socket
	hostname = socket.gethostname()
	bf.write("# hostname: "+hostname+"\n")
	import getpass
	bf.write("# user: "+getpass.getuser()+"\n")
	import sys
	bf.write("# python version: "+sys.version.replace("\n","")+"\n")
	bf.write("# python executable: "+sys.executable+"\n")

	bf.write("\n\n{\n")
	t = "\t"
	n = "\n"
	for k,v in args.items():
		if k in ('output'):
			v = v.name
		if isinstance(v, str):
			v = '"'+v+'"'
		k = '"'+k+'"'
		bf.write(t + str(k) + " : " + str(v) + ",\n")
	bf.write("}\n")
	bf.close()

def load_from_backup(args):
	bf = args["continue_from_backup"]
	try:
		nargs = eval(bf.read())
		bf.close()
		assert set(nargs.keys())==set(args.keys())
	except (SyntaxError, AssertionError) as e:
		sys.exit("Error in backup file. Make sure it's really a backup file\n"
		"from current version of ConcordanceCrawler.")

	load = load_from_corpus(nargs['output'],nargs['format'])
	nargs['output'] = open(nargs['output'], 'a')

	return nargs, load

def main():

	args, mode = get_args()
	if mode == "run":
		save_backup(args)
	elif mode == "backup":
		args, load = load_from_backup(args)
	else:
		assert False, "error, undefined mode"

	# setup command-line arguments and get them from user
	words = args["word"]
	number = args["number_of_concordances"]
	baz = args["bazword_generator"]
	max_per_page = args["max_per_page"]
	page_limited = True if max_per_page else False
	bufsize = args["buffer_size"]
	if baz=="RANDOM":
		bazgen = RandomShortWords()
	elif baz=="WIKI_ARTICLES":
		bazgen = WikipediaRandomArticle()
	elif baz=="WIKI_TITLES":
		bazgen = WikipediaRandomArticleTitles()
	elif baz=="NUMBERS":
		bazgen = IncreasingNumbers()

	log_level = ["DEBUG","DETAILS","STATUS","ERROR"][args['verbosity']]


	lc = EnglishLoggingCrawler(bazgen,bufsize=bufsize)
	if mode == 'backup':
		lc.visited_pages = load['links']
		lc.crawled_concordances = load['concordances']
		lc.num_concordances = load['maxid']

	pos = args['part_of_speech']
	use_textblob_lemmatizer(lc, pos)

	# setup logger
	setup_logger(log_level)

	# here is output formatter
	of = create_formatter(
		format=args["format"],
		output_stream=args["output"],
		extending=False if mode=="run" else True
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
	except KeyboardInterrupt as e:
		print(format_exc(e))
		lc.log_state()
		logging.info("\n\nConcordanceCrawler aborted, you can try to find " +
		"its output in " + args["output"].name)
	finally:
		# close output stream
		of.close()

if __name__=="__main__":
	main()
