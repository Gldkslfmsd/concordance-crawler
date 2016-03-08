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
	def __init__(self, word, bazgen):
		super(WiseExceptionHandlingCrawler, self).__init__(word, bazgen)
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
	

class LoggingCrawler(WiseExceptionHandlingCrawler):	
	'''Crawls concordances and logs statistics'''

	def __init__(self, word, bazgen):
		super(LoggingCrawler, self).__init__(word,bazgen)
		self._raw_filter_link = self.filter_link
		self.filter_link = self.filter_link_logwrapper

	def filter_link_logwrapper(self,link):
		res = self._raw_filter_link(link)
		if not res:
			self.Logger.info('link {0} rejected'.format(link))
		return res

	def crawl_links(self):
		links = super(LoggingCrawler, self).crawl_links()
		self.log_details("crawled SERP, parsed {0} links".format(
			len(links)))
		return links

	def _yield_concordances_from_link(self, link):
		self.Logger.debug("trying to download {0}".format(link['link']))
		for l in super(LoggingCrawler, self)._yield_concordances_from_link(link):
			self.num_concordances += 1
			yield l


	def visit_link(self, link):
		try:
			concordances = super(LoggingCrawler, self).visit_link(link)
		except requests.exceptions.Timeout:
			logging.error("request {0} cannot be handled for a long time".format(
				link['link']))
			self.page_errors += 1
			raise
		except requests.exceptions.RequestException as e:
			logging.error("\'{}\' occured during getting {}".format(
				e,link['link']))
			self.page_errors += 1
			raise
		except Exception:
			self.Logger.error("!!! Undefined error occured, {0}".format(format_exc()))
			self.page_errors += 1
			raise
		else:
			self.log_details("page {0} visited, {1} concordances found".format(
				link['link'],len(concordances)))
			# because of statistics (is not thread-safe)
			self.num_pages += 1
			return concordances



# TODO
#class SimpleLoggingCrawler(LoggingCrawler):
#	def __init__(self, word, bazgen):
#		super(SimpleLoggingCrawler, self).__init__(word,bazgen)
