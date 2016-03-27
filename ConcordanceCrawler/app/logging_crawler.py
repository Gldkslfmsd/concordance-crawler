from ConcordanceCrawler.core.concordance_crawler import *
from ConcordanceCrawler.core.links import SERPError
import six
if six.PY3:
	import sys
	if sys.version_info.minor>=4:
		from multiprocessing.context import TimeoutError as multiprocessing_TimeoutError
	else:
		from multiprocessing import TimeoutError as multiprocessing_TimeoutError

elif six.PY2:
	from multiprocessing import TimeoutError as multiprocessing_TimeoutError
	from requests.exceptions import ConnectionError
import requests

from ConcordanceCrawler.core.limited_buffer import LimitedBuffer
import re

'''This class is used just by demo commandline application.
'''

from traceback import format_exc

def setup_logger(log_level):
	# "shut down" the logger from requests module
	#logging.getLogger("requests").setLevel(logging.WARNING)
	# setup this logger:
	logging.addLevelName(DETAILS,"DETAILS")
	logging.addLevelName(STATUS,"STATUS")
	logging.basicConfig(level=log_level,
		format="%(asctime)-15s %(levelname)s: %(message)s")
	logging.getLogger("requests").setLevel(logging.WARNING)

class WiseExceptionHandlingCrawler(ConcordanceCrawler):
	'''Crash when there is too much of RequestExceptions'''

	def __init__(self, words, bazgen):
		super(WiseExceptionHandlingCrawler, self).__init__(words, bazgen)
		exc_handler = [
			(requests.exceptions.RequestException, self.handle_connection_error),
			(SERPError, self.handle_serp_error),
			]


		for e,h in exc_handler:
			self.set_exception_handler(e,h)

	def handle_serp_error(self, e):
		self.Logger.error("SERP error")
		self.serp_errors += 1
		self.log_state()
		self.handle_connection_error(e)

	def handle_connection_error(self, e):
		if self.serp_errors>10:
			self.Logger.critical('aborting crawler due to high number of serp errors')
			self.crawling_allowed = False

# logging levels
DETAILS = logging.INFO-5
STATUS = logging.INFO

class Logging(object):
	def __init__(self):
		self.links_filtered = 0
		self.num_serps = 0 # number of serp (search engine result pages) downloaded
		self.serp_errors = 0
		self.num_pages = 0 # number of visited pages
		self.page_errors = 0 # number of errors during visiting pages
		self.num_concordances = 0 # number of found concordances
		self.links_filtered_suffix = 0
		self.links_filtered_rep = 0
		self.repeated_concordances = 0
		self.page_lan_filtered = 0
		self.links_crawled = 0


	def log_details(self,*a):
 		self.Logger.log(DETAILS, *a)

	def log_state(self):
		'logs interesting numbers about progress'''
		self.Logger.info("""Crawling status 
serp\t\t{num_serps} ({serp_errors} errors) 
links crawled\t{num_links} ({suffix} filtered because of format suffix, {rep} crawled repeatedly)
pages visited\t{num_pages} ({lan_filter} filtered by language filter, {page_errors} errors)
concordances\t{num_concordances} ({more_times} crawled repeatedly)""".format(
			num_serps=self.num_serps,
			serp_errors=self.serp_errors,
			num_links=self.links_crawled,
			suffix=self.links_filtered_suffix,
			rep=self.links_filtered_rep,
			num_pages=self.num_pages,
			links_filtered=self.links_filtered,
			lan_filter=self.page_lan_filtered,
			page_errors=self.page_errors,
			num_concordances=self.num_concordances,
			more_times=self.repeated_concordances,
		)
	)

	# briefer version of log_state (could be sometimes useful)
	# self.brief_log_state()

	#	def brief_log_state(self):
	#		logging.info(
	#			("Successfully crawled {num_concordances} concordances from {total_concordances} "+
	#			"({percent}%)").format(
	#			num_concordances=self.num_concordances,
	#			total_concordances = self.total_concordances,
	#			percent = self.num_concordances/self.total_concordances*100))
	
	

class LoggingCrawler(WiseExceptionHandlingCrawler, Logging):	
	'''Crawls concordances and logs statistics'''

	def __init__(self, words, bazgen=None):
		super(LoggingCrawler, self).__init__(words,bazgen)
		Logging.__init__(self)
		self._raw_filter_link = self.filter_link
		self.filter_link = self.filter_link_logwrapper
		self.Logger = logging.getLogger().getChild('ConcordanceCrawlerLogger')
		self.Logger.setLevel(50) # mutes all warnings and logs # TODO: why?

		self._raw_language_filter = self.visitor.language_filter
		self.visitor.language_filter = self.language_filter_log_wrapper

		self.visited_pages = LimitedBuffer()
		self.crawled_concordances = LimitedBuffer()

	def language_filter_log_wrapper(self, text):
		res = self._raw_language_filter(text)
#		for manual testing of accuracy of language filter
#		import re
#		text = re.sub(r"\n+",r"\n",text,flags=re.M)
#		import random
#		f = open(("yes" if res else "no") + "/text"+str(random.random()),"w")
#		f.write(text)
#		f.close()
		if res:
			return True
		self.Logger.debug("page rejected by language filter")
		self.page_lan_filtered += 1
		self.log_state()
		return False

	def modify_concordance(self, con):
		'''adds id to every concordance
		change \n to spaces, delete more than two following spaces'''
		con['id'] = self.num_concordances
		c = con["concordance"].strip()
		c = re.sub(r"\s"," ",c,flags=re.UNICODE | re.MULTILINE)
		c = re.sub(r" +"," ",c)
		con["concordance"] = c
		return con

	def yield_concordances(self, words):
		for con in super(LoggingCrawler, self).yield_concordances(words):
			con = self.modify_concordance(con)
			yield con

	def filter_link_logwrapper(self,link):
		res = self._raw_filter_link(link)
		if not res:
			self.Logger.debug('link {0} rejected because of format suffix'.format(link))
			self.links_filtered_suffix += 1
			self.log_state()
			return False
		if self.visited_pages.contains(link):
			self.Logger.debug('link {0} rejected because it has already been visited'.format(link))
			self.links_filtered_rep += 1
			self.log_state()
			return False
		return True

	def crawl_links(self):
		links = super(LoggingCrawler, self).crawl_links()
		self.num_serps += 1
		self.log_details("crawled SERP, parsed {0} links".format(
			len(links)))
		self.links_crawled += len(links)
		self.log_state()
		return links

	def _yield_concordances_from_link(self, link):
		self.Logger.debug("trying to download {0}".format(link['link']))
		for c in super(LoggingCrawler, self)._yield_concordances_from_link(link):
			# repeatedly crawled concordances are filtered here
			if not self.crawled_concordances.contains(c["concordance"]):
				self.crawled_concordances.insert(c["concordance"])
				self.num_concordances += 1
				self.log_state()
				yield c
			else:
				self.log_details("following concordance crawled repeatedly {0}".format(c))
				self.repeated_concordances += 1
				self.log_state()


	def concordances_from_link(self, link):
		try:
			concordances = super(LoggingCrawler, self).concordances_from_link(link)
		except requests.exceptions.Timeout:
			self.Logger.error("request {0} cannot be handled for a long time".format(
				link['link']))
			self.page_errors += 1
			raise
		except requests.exceptions.RequestException as e:
			self.Logger.error("\'{}\' occured during getting {}".format(
				e,link['link']))
			self.page_errors += 1
			raise
		except TypeError:
			self.Logger.error("parsing error during processing \'{}\'".format(
				link['link']))
			self.page_errors += 1
		except Exception:
			self.Logger.error("!!! Undefined error occured, {0}".format(format_exc()))
			self.page_errors += 1
			raise
		else:
			self.visited_pages.insert(link['link'])
			self.log_details("page {0} visited, {1} concordances found".format(
				link['link'],len(concordances)))
			# because of statistics (is not thread-safe)
			self.num_pages += 1
			return concordances



# TODO
#class SimpleLoggingCrawler(LoggingCrawler):
#	def __init__(self, word, bazgen):
#		super(SimpleLoggingCrawler, self).__init__(word,bazgen)
