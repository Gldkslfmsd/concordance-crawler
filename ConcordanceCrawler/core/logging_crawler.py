
from ConcordanceCrawler.core.concordance_crawler import *
from ConcordanceCrawler.core.links import SERPError
from ConcordanceCrawler.core.urlrequest import UrlRequestException
from ConcordanceCrawler.core.visitor import VisitTooLongException
import requests
import logging

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

# logging levels
DETAILS = logging.INFO-5
STATUS = logging.INFO

class Logging(object):
	'''Logging for LoggingCrawler. It adds many counters for logging of status.'''
	def __init__(self):
		self.allow_logging = True
		self.Logger = logging.getLogger().getChild('ConcordanceCrawlerLogger')
		self.Logger.setLevel(logging.DEBUG)  # logger is on by default
		  
		self.num_serps = 0 # number of serp (search engine result pages) downloaded
		self.serp_errors = 0
		self.num_pages = 0 # number of visited pages
		self.page_errors = 0 # number of errors during visiting pages
		self.num_concordances = 0 # number of found concordances
		self.links_filtered = 0
		self.links_filtered_rep = 0
		self.repeated_concordances = 0
		self.page_enc_filtered = 0
		self.page_lan_filtered = 0
		self.links_crawled = 0


	def log_details(self,*a):
 		self.Logger.log(DETAILS, *a)

	def log_state(self):
		'''logs interesting numbers about progress'''

		if self.allow_logging:
			self.Logger.setLevel(10)
		else:
			self.Logger.setLevel(50)
		
		self.Logger.info("""Crawling status 
serp\t\t{num_serps} ({serp_errors} errors) 
links crawled\t{num_links} ({links_filtered} filtered, {rep} crawled repeatedly)
pages visited\t{num_pages} ({enc_filter} filtered by encoding filter, {lan_filter} filtered by language filter, {page_errors} errors)
concordances\t{num_concordances} ({more_times} crawled repeatedly)""".format(
			num_serps=self.num_serps,
			serp_errors=self.serp_errors,
			num_links=self.links_crawled,
			links_filtered=self.links_filtered,
			rep=self.links_filtered_rep,
			num_pages=self.num_pages,
			enc_filter=self.page_enc_filtered,
			lan_filter=self.page_lan_filtered,
			page_errors=self.page_errors,
			num_concordances=self.num_concordances,
			more_times=self.repeated_concordances,
		)
	)
	
class LoggingCrawler(ConcordanceCrawler, Logging):	
	'''Crawls concordances, logs progress and statistics and handles errors and exceptions
	
	Most of its methods only call parent's methods and add logging and error handling.
	'''
	
	# add allow_logging to configurable attributes
	attributes = ConcordanceCrawler.attributes + ['allow_logging']
	
	# recommended logging format, it includes date to log message
	log_format = "%(asctime)-15s %(levelname)s: %(message)s"

	def __init__(self, bazgen=None, bufsize=None):
		super(LoggingCrawler, self).__init__(bazgen)
		Logging.__init__(self)


		if bufsize is None:
			sizearg = ()  # empty tuple
		else:
			sizearg = (bufsize,)
		self.visited_pages = LimitedBuffer(*sizearg)
		self.crawled_concordances = LimitedBuffer(*sizearg)

		self._raw_filter_link = self.filter_link
		self.filter_link = self.filter_link_logwrapper

		self._raw_language_filter = self.visitor.language_filter
		self.visitor.language_filter = self.language_filter_log_wrapper

		self._raw_norm_encoding = self.visitor.norm_encoding
		self.visitor.norm_encoding = self.norm_encoding

	def norm_encoding(self, document, headers):
		res = self._raw_norm_encoding(document, headers)
		if not res:
			self.Logger.debug("page rejected by encoding filter")
			self.page_enc_filtered += 1
		return res

	def language_filter_log_wrapper(self, text):
		res = self._raw_language_filter(text)
		"""
#		for manual testing of accuracy of language filter
#		import re
#		text = re.sub(r"\n+",r"\n",text,flags=re.M)
#		import random
#		f = open(("yes" if res else "no") + "/text"+str(random.random()),"w")
#		f.write(text)
#		f.close()
		"""
		if res:
			return True
		self.Logger.debug("page rejected by language filter")
		self.page_lan_filtered += 1
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
			self.links_filtered += 1
			self.log_state()
			return False
		if self.visited_pages.contains(link):
			self.Logger.debug('link {0} rejected because it has already been visited'.format(link))
			self.links_filtered_rep += 1
			self.log_state()
			return False
		return True

	def get_links(self, *args, **kwargs):
		links = []
		try:
			links = super(LoggingCrawler, self).get_links(*args, **kwargs)
		except SERPError:
			self.Logger.error("SERP error")
			self.serp_errors += 1
			self.log_state()
		else:
			self.num_serps += 1
			self.log_details("crawled SERP, parsed {0} links".format(
				len(links)))
			self.links_crawled += len(links)
			self.log_state()
		
		self.stopping_criterion()
		return links

	def _yield_concordances_from_link(self, link, words):
		self.Logger.debug("trying to download {0}".format(link))
		for c in super(LoggingCrawler, self)._yield_concordances_from_link(link, words):
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


	def concordances_from_link(self, link, words):
		try:
			concordances = super(LoggingCrawler, self).concordances_from_link(link, words)
		except (requests.exceptions.RequestException, UrlRequestException) as e:
			self.Logger.error("\'{}\' occured during getting {}".format(
				e,link))
			self.page_errors += 1
		except VisitTooLongException:
			self.Logger.error("processing of \'{}\' took too long".format(
				link))
			self.page_errors += 1
		except KeyboardInterrupt:  # terminate whole application
			raise
		except Exception:
			self.Logger.error("!!! Unknown error occured, {0}".format(format_exc()))
			self.page_errors += 1
		else:
			self.visited_pages.insert(link)
			self.log_details("page {0} visited, {1} concordances found".format(
				link,len(concordances)))
			self.num_pages += 1
			self.log_state()
			return concordances

	def stopping_criterion(self):
		'''if crawling is unperspective or there is some error with SE, 
		assign False to self.crawling_allowed here and crawler will be aborted soon.
		'''
		if self.serp_errors > 10:
			self.Logger.critical('aborting crawler due to high number of serp errors')
			self.crawling_allowed = False


# sealed
class EnglishLoggingCrawler(LoggingCrawler):
	'''This class is used by ConcordanceCrawler command-line application. 
	
	It should be a sealed class, I don't recommend anyone to inherit from it, because it uses a dirty trick
	with `after_setup` which may won't work in child class after reconfiguring `language_filter` etc..
	'''
	def __init__(self, bazgen=None, bufsize=None):
		super(EnglishLoggingCrawler, self).__init__(bazgen=bazgen, bufsize=bufsize)
	
	def after_setup(self, **kwargs):
		if 'filter_link' in kwargs:
			self._raw_filter_link = self.filter_link
			self.filter_link = self.filter_link_logwrapper
	
		if 'language_filter' in kwargs:
			self._raw_language_filter = self.visitor.language_filter
			self.visitor.language_filter = self.language_filter_log_wrapper
	
		if 'norm_encoding' in kwargs:
			self._raw_norm_encoding = self.visitor.norm_encoding
			self.visitor.norm_encoding = self.norm_encoding
	
	def stopping_criterion(self):
		super(EnglishLoggingCrawler, self).stopping_criterion()
		if self.num_serps >= 10 and self.num_concordances <= 1:
			self.Logger.critical('aborting crawler because this job seems unperspective')
			self.crawling_allowed = False