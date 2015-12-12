import six
from traceback import format_exc
import logging
import requests
if six.PY3:
	import sys
	if sys.version_info.minor>=4:
		from multiprocessing.context import TimeoutError as multiprocessing_TimeoutError
	else:
		from multiprocessing import TimeoutError as multiprocessing_TimeoutError
elif six.PY2:
	from multiprocessing import TimeoutError as multiprocessing_TimeoutError

from ConcordanceCrawler.core.links import *
from ConcordanceCrawler.core.visitor import *
from ConcordanceCrawler.core.bazwords import *
from ConcordanceCrawler.core.visible_text import filter_link

# logging levels
DETAILS = logging.INFO-5
STATUS = logging.INFO

class Loggable(object):
	def log_details(self,*a):
 		self.Logger.log(DETAILS, *a)

	def log_state(self):
		'logs interesting numbers about progress'''
		self.Logger.info("""Crawling status 
serp\t\t{num_serps} ({serp_errors} errors) 
pages visited\t{num_pages} ({unique_pages} unique pages, {page_errors} errors)
concordances\t{num_concordances}""".format(
			num_serps=self.num_serps,
			serp_errors=self.serp_errors,
			num_pages=self.num_pages,
			unique_pages=len(self.unique_links),
			page_errors=self.page_errors,
			num_concordances=self.num_concordances
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
	
	
class CrawlerConfigurator(object):
	'''configurable attributes of ConcordanceCrawler can be set via
	this method'''

	def setup(self, **kwargs):
		visitor = Visitor()
		for atr in kwargs.keys():
			if atr in Visitor.attributes:
				setattr(visitor, atr, kwargs[atr])
			elif atr in ConcordanceCrawler.attributes:
				setattr(self, atr, kwargs[atr])
			else:
				raise AttributeError("Attribute '{0}' is not known and cannot be set.".format(atr))
		self.visitor = visitor
	


class ConcordanceCrawler(Loggable, CrawlerConfigurator):	
	attributes = ["bazgen", "Logger","filter_link"]

	num_serps = 0 # number of serp (search engine result pages) downloaded
	serp_errors = 0
	num_pages = 0 # number of visited pages
	page_errors = 0 # number of errors during visiting pages
	num_concordances = 0 # number of found concordances

	def __init__(self, word, bazgen=None):
		self.word = word
		if bazgen:
			self.bazgen = bazgen
		else:
			self.bazgen = RandomShortWords()
		# this is set of visited links, we want to count them because of logging
		self.filter_link = filter_link
		self.unique_links = set()
		self.Logger = logging.getLogger().getChild('ConcordanceCrawlerLogger')
		self.Logger.setLevel(50) # mutes all warnings and logs
		self.visitor = Visitor() # it will work even without setup
		self.page_limited = False
		self._exceptions_handlers = dict()
		self._ignored_exceptions = set()

		# if False, yield links ends
		self.crawling_allowed = True

	def yield_concordances(self,word):
		'''Generator crawling concordances'''

		for link in self._yield_links():
#			link['link'] = 'http://gimli.ms.mff.cuni.cz/////'
			if not self.crawling_allowed:
				break
			for con in self._yield_concordances_from_link(link):
				self.log_state()
				yield con

	def _yield_links(self):
		'''Generator yielding links from search engine result page. It scrapes
		one serp, parses links and then yields them. Then again.
		'''
		while self.crawling_allowed:
			try:
				try:
					links = crawl_links(self.word,1,self.bazgen)
					self.num_serps += 1
				except multiprocessing_TimeoutError:
					self.Logger.error("SERP cannot be handled for a long time")
					self.serp_errors += 1
					self.log_state()
					raise
				except requests.exceptions.RequestException as e:
					self.serp_errors += 1
					logging.error("\'{0}\' occured".format(e))
					self.log_state()
					raise
				except:
					self.Logger.error("!!! Undefined error occured, {0}".format(format_exc()))
					self.serp_errors += 1
					self.log_state()
					raise
				else:
					self.log_details("crawled SERP, parsed {0} links".format(
						len(links)))
					for l in links:
						# todo: maybe move this to links crawling
						if self.filter_link(l["link"]):
							yield l
						else:
							self.Logger.info('link {0} rejected'.format(l['link']))
			except Exception as e:
				if any((issubclass(type(e),t) for t in self._exceptions_handlers.keys())):
					self._handle_exception(e)
				elif all(not issubclass(type(e),t) for t in self._ignored_exceptions):
					raise

	def set_exception_handler(self, exc_class, handler):
		if exc_class in self._ignored_exceptions:
			raise Exception("cannot set exception handler on '{0}', it's already among "
				"ignored exceptions".format(exc_class))
		self._exceptions_handlers[exc_class] = handler

	def ignore_exception(self,exc_class):
		if exc_class in self._exceptions_handlers.keys():
			raise Exception("cannot ignore exception '{0}', it's already among "
				"handled exceptions".format(exc_class))
		self._ignored_exceptions.add(exc_class)

	def _handle_exception(self,exc):
		'''finds the most suitable exception handler and calls it'''
		mro = type(exc).mro()
		for c in mro:
			if c in self._exceptions_handlers.keys():
				self._exceptions_handlers[c](exc)
				return
		print("handler is not found")

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
			try:
				self.Logger.debug("trying to download {0}".format(l['link']))
				# here is the link visited
				concordances = self.visitor.visit_links([l],self.word)
				# add url to set of unique links, because we want to count them
				self.unique_links.add(l['link'])
				self.log_details("page {0} visited, {1} concordances found".format(
					l['link'],len(concordances)))
				# because of statistics (is not thread-safe)
				self.num_pages += 1
			except multiprocessing_TimeoutError:
				logging.error("request {0} cannot be handled for a long time".format(
					l['link']))
				self.page_errors += 1
				raise
			except requests.exceptions.RequestException as e:
				logging.error("\'{}\' occured during getting {}".format(
					e,l['link']))
				self.page_errors += 1
				raise
			except Exception:
				self.Logger.error("!!! Undefined error occured, {0}".format(format_exc()))
				self.page_errors += 1
				raise
			else:
				for i,c in enumerate(concordances):
					# maximum limit of concordances per page reached
					if self.page_limited and i>self.max_per_page:
						break
					# here is formed the output structure for concordance
					res = c
					self.num_concordances += 1
					yield res
		except Exception as e:
			if any((issubclass(type(e),t) for t in self._exceptions_handlers.keys())):
				self._handle_exception(e)
			elif all(not issubclass(type(e),t) for t in self._ignored_exceptions):
				raise

		






if __name__=='__main__':
	print("ahoj")
	#setup_logger(0)
	x = ConcordanceCrawler("exception", RandomShortWords())
	try:
		x.setup(abc="nic")
	except AttributeError:
		print("it's ok")
	import ConcordanceCrawler.core.language_analysis as language_analysis
	def mypredict(*a, **kw):
		print("mypredict is called!")
		return language_analysis.predict_language(*a,**kw)
	x.setup(predict_language = mypredict)
	x.log_state()

	for i in x._yield_concordances_from_link({"link":'https://docs.python.org/2/library/exceptions.html'}):
		print(i)
	print("done")
