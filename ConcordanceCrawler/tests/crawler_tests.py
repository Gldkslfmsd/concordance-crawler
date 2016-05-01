import unittest

from ConcordanceCrawler.core.concordance_crawler import *
from ConcordanceCrawler.core.logging_crawler import *

from ConcordanceCrawler.core.bazwords import IncreasingNumbers
import re

class A(Exception):
	pass

class B(A):
	pass

x = 0
h = 0
def raise_error(_):
	global x
	x += 1
	if x<2:	
		raise B()
	return "scrape "*10

def handler(_):
	global h
	h = 1

problem = {
"url": "http://www.spearfuneralhome.net/displayfuneral.php?item=205&letter=", 
"date": "2016-03-15 20:29:14.640150", 
"concordance": "And Athena, goddess of wisdom to store the fate of mankind and quietly on the bottom of this box positive things \"hope\" too little time for fly as well as, positioned the [url=http://www.filsfils.com/]http://www.filsfils.com/[/url] \rones own style.", 
"id": 7, 
"keyword": "fly"
}


common_words = ["a","the","in","of","at","to"]
class TestCrawler(unittest.TestCase):
	def test_modify_concordance(self):
		crawler = LoggingCrawler(common_words)
		c = crawler.modify_concordance(problem)
		m = re.match(r"\r|\s+",c["concordance"])
		self.assertIsNone(m)


# TODO
	"""
	def test_setting_handler_fails(self):
		crawler = ConcordanceCrawler(common_words)
		# test that you cannot set handler on ignored exception
		crawler.ignore_exception(A)
		self.assertRaises(Exception, crawler.set_exception_handler, A, None)

	def test_ignoring_exception_fails(self):
		crawler = ConcordanceCrawler(common_words)
		# you cannot ignore exception that already has handler
		crawler.set_exception_handler(B, handler)
		self.assertRaises(Exception, crawler.ignore_exception, B)

	def test_exception_handler_works(self):
		for exp in (B, A):
			# test that handler for exception is really called
			global h,x
			x = 0
			crawler = ConcordanceCrawler(common_words)
			crawler.setup(get_raw_html=raise_error, language_filter=lambda _: True)
			crawler.set_exception_handler(exp, handler)
			c = zip(crawler.yield_concordances("scrape"), range(3))
			c = list(c) # raises B and calls handler
			self.assertEqual(h,1)
			x = 0
			h = 0


	def test_ignoring_exceptions(self):
		crawler = ConcordanceCrawler(common_words)
		crawler.setup(get_raw_html=raise_error, language_filter=lambda _: True)

		crawler.ignore_exception(B)
		c =  zip(crawler.yield_concordances("scrape"), range(3))
		# it shouldn't raise any exception, but self.assertNotRaises doesn't exist
		try:
			list(c)
		except:
			assert False, 'test_ignoring_exceptions failed'

	def test_ignoring_derived_exceptions(self):
		'''A is ignored, but its subclass, B, is raised'''
		crawler = ConcordanceCrawler(common_words)
		crawler.setup(get_raw_html=raise_error, language_filter=lambda _: True)

		crawler.ignore_exception(A)
		c =  zip(crawler.yield_concordances("scrape"), range(3))
		try:
			list(c)
		except:
			assert False, 'test_ignoring_exceptions failed'

	def test_abort_crawling(self):
		crawler = ConcordanceCrawler(common_words)
		crawler.bazgen = IncreasingNumbers()
		# crawling can continue after abortion
		c = list(zip(crawler.yield_concordances("a"), range(1)))
		self.assertNotEqual(c,[])
#		c = zip(crawler.yield_concordances("a"), range(2))
#		self.assertNotEqual(list(c),[])

		# when crawling_allowed = False, it crawls nothing
		crawler.crawling_allowed = False
		c = list(zip(crawler.yield_concordances("a"), range(2)))
		self.assertEqual(c,[])

		# but it can continue
		crawler.crawling_allowed = True
		c = list(zip(crawler.yield_concordances("a"), range(1)))
		self.assertNotEqual(c,[])





		




"""
