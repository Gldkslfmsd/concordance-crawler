import six

from traceback import format_exc
import logging
import requests
if six.PY3:
	from multiprocessing.context import TimeoutError as multiprocessing_TimeoutError
elif six.PY2:
	from multiprocessing import TimeoutError as multiprocessing_TimeoutError
	from requests.exceptions import ConnectionError

from ConcordanceCrawler.core.links import *
from ConcordanceCrawler.core.visitor import *

'''This class is used just by demo commandline application.
'''

# logging levels
DETAILS = logging.INFO-5
STATUS = logging.INFO

def log_details(*a):
 logging.log(DETAILS, *a)

def setup_logger(log_level):
	# "shut down" the logger from requests module
	#logging.getLogger("requests").setLevel(logging.WARNING)
	# setup this logger:
	logging.addLevelName(DETAILS,"DETAILS")
	logging.addLevelName(STATUS,"STATUS")
	logging.basicConfig(level=log_level,
		format="%(asctime)-15s %(levelname)s: %(message)s")
	logging.getLogger("requests").setLevel(logging.WARNING)

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
		# this is set of visited links, we want to count them because of logging
		self.unique_links = set()
		self.visitor = Visitor()

	def log_state(self):
		'''logs interesting numbers about progress'''
		logging.info("""Crawling status 
	serp\t\t{num_serps} ({serp_errors} errors) 
	pages visited\t{num_pages} ({unique_pages} unique pages, {page_errors} errors)
	concordances\t{num_concordances}""".format(
			num_serps=self.num_serps,
			serp_errors=self.serp_errors,
			num_pages=self.num_pages,
			unique_pages=len(self.unique_links),
			page_errors=self.page_errors,
			num_concordances=self.num_concordances))

	# briefer version of log_state (could be sometimes useful)
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

		for link in self._yield_links():
			for con in self._yield_concordances_from_link(link):
				self.log_state()
				yield con

	def _yield_links(self):
		'''Generator yielding links from search engine result page. It scrapes
		one serp, parses links and then yields them. Then again.
		'''
		while True:
			try:
				links = crawl_links(self.word,1,self.bazgen)
				self.num_serps += 1
			except multiprocessing_TimeoutError:
				logging.error("SERP cannot be handled for a long time")
				self.serp_errors += 1
				self.log_state()
			except (requests.exceptions.RequestException, ConnectionError) as e:
				self.serp_errors += 1
				logging.error("\'{}\' occured".format(e))
				self.log_state()
			except Exception:
				logging.error("!!! Undefined error occured, {}".format(format_exc()))
				self.serp_errors += 1
				self.log_state()
			else:
				log_details("crawled SERP, parsed {} links".format(
					len(links)))
				for l in links:
					yield l

	def _yield_concordances_from_link(self,l):
		'''This generator gets link as an argument, downloads the page, parses
		concordances and yields them. Besides that it logs progress.

		Args:
			l -- link, a dictionary structure coming from module visitor of
			ConcordanceCrawler
		'''
		# this comments are for debugging:
		#l['link']='https://www.diffchecker.com/'
		#l['link']='http://en.bab.la/dictionary/english-hindi/riding'
		#print("link:",l['link'])
		try:
			logging.debug("trying to download {}".format(l['link']))
			# here is the link visited
			concordances = self.visitor.visit_links([l],self.word)
			# add url to set of unique links, because we want to count them
			self.unique_links.add(l['link'])
			log_details("page {} visited, {} concordances found".format(
				l['link'],len(concordances)))
			# because of statistics (is not thread-safe)
			self.num_pages += 1
		except multiprocessing_TimeoutError:
			logging.error("request {} cannot be handled for a long time".format(
				l['link']))
			self.page_errors += 1
		except (requests.exceptions.RequestException, ConnectionError) as e:
			logging.error("\'{}\' occured during getting {}".format(
				e,l['link']))
			self.page_errors += 1
		except Exception:
			logging.error("!!! Undefined error occured, {}".format(format_exc()))
			self.page_errors += 1
		else:
			for i,c in enumerate(concordances):
				# maximum limit of concordances per page reached
				if self.page_limited and i>self.max_per_page:
					break
				# here is formed the output structure for concordance
				res = c
				self.num_concordances += 1
				yield res


