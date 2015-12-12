from ConcordanceCrawler.core.concordance_crawler import *
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
		self.set_exception_handler(requests.exceptions.RequestException, self.handle_connection_errors)

	#	self.c = 0
	#	self.setup(get_raw_html=self.buggy_requests)

#	def buggy_requests(self,link):
#		self.c += 1
#		if self.c % 3 !=0:
#			raise requests.exceptions.ConnectionError("TESTING ERROR")
#		return requests.get(link).text

	def handle_connection_errors(self, e):
		if self.serp_errors>10 or self.page_errors>10:
			self.Logger.critical('aborting crawler due to high number of serp or page errors')
			self.crawling_allowed = False
	

class LoggingCrawler(WiseExceptionHandlingCrawler):	
	'''Crawls concordances and logs statistics'''

	def __init__(self, word, bazgen):
		super(LoggingCrawler, self).__init__(word,bazgen)


class SimpleLoggingCrawler(LoggingCrawler):
	def __init__(self, word, bazgen):
		super(SimpleLoggingCrawler, self).__init__(word,bazgen)
