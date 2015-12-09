from ConcordanceCrawler.core.concordance_crawler import *

'''This class is used just by demo commandline application.
'''

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
	
	def __init__(self, word, bazgen):
		super(WiseExceptionHandlingCrawler, self).__init__(word, bazgen)
	

class LoggingCrawler(ConcordanceCrawler):	
	'''Crawls concordances and logs statistics'''

	def __init__(self, word, bazgen):
		super(LoggingCrawler, self).__init__(word,bazgen)



class SimpleLoggingCrawler(LoggingCrawler):
	def __init__(self, word, bazgen):
		super(SimpleLoggingCrawler, self).__init__(word,bazgen)
