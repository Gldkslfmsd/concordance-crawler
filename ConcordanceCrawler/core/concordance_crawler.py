from traceback import format_exc
import logging
import requests
import ConcordanceCrawler.core.links as links
from ConcordanceCrawler.core.links import filter_link_by_format
from ConcordanceCrawler.core.visitor import *
from ConcordanceCrawler.core.bazwords import *

class CrawlerConfigurator(object):
	'''configurable attributes of ConcordanceCrawler can be set via
	this method'''

	def setup(self, **kwargs):
		visitor = self.visitor 
		for atr in kwargs.keys():
			if atr in Visitor.attributes:
				setattr(visitor, atr, kwargs[atr])
			elif atr in ConcordanceCrawler.attributes:
				setattr(self, atr, kwargs[atr])
			else:
				raise AttributeError("Attribute '{0}' is not known and cannot be set.".format(atr))
		self.after_setup(**kwargs)

	def after_setup(self,**kwargs):
		pass

	
class ConcordanceCrawler(CrawlerConfigurator):	
	attributes = ["bazgen", "filter_link"]

	def __init__(self, bazgen=None):

		if bazgen:
			self.bazgen = bazgen
		else:
			self.bazgen = RandomShortWords()
		self.visitor = Visitor()
		self.page_limited = False

		# if False, yield links ends
		self.crawling_allowed = True

		# this is another method
		self.filter_link = filter_link_by_format


	def yield_concordances(self,words):
		'''Generator crawling concordances		
		words: a list of strings, words, whose concordances should be
		crawled. It should be a single word, or a single word and its other forms.
		The first one is considered as a basic form, links will be found only
		with this form.'''

		canonical_form = words[0]
		for link in self._yield_links(canonical_form):
#			link['link'] = 'http://gimli.ms.mff.cuni.cz/////'
			if not self.crawling_allowed:
				break
			for con in self._yield_concordances_from_link(link, words):
				yield con

	def _yield_links(self, keyword):
		'''Generator yielding links from search engine result page. It scrapes
		one serp, parses links and then yields them. Then again.
		'''
		while self.crawling_allowed:
			links = self.crawl_links(keyword)
			for l in links:
				if self.filter_link(l["link"]):
					yield l

	def crawl_links(self, keyword):
		'''
		returns: list of links, it can be empty
		raises: SERPError
		'''
		return links.crawl_links(keyword, bazword_gen=self.bazgen)

	def concordances_from_link(self, link, words):
		return self.visitor.concordances_from_link(link, words)

	def _yield_concordances_from_link(self,l, words):
		'''This generator gets link as an argument, downloads the page, parses
		concordances and yields them.

		Args:
			l -- link, a dictionary structure coming from module visitor of
			ConcordanceCrawler
		'''
		# here is the link visited
		concordances = self.concordances_from_link(l, words)
		if not concordances:
			return
		for i,c in enumerate(concordances):
			# maximum limit of concordances per page reached
			if self.page_limited and i==self.max_per_page:
				break
			# here is formed the output structure for concordance
			res = c
			yield res







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
