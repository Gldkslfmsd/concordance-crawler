import unittest

from ConcordanceCrawler.core.concordance_crawler import *

class OKException(Exception):
	pass

class EverythingIsOK(OKException):
	pass

x = 0
def raise_error(_):
	global x
	x += 1
	if x<2:	
		raise EverythingIsOK()
	return "scrape scrape scrape"

h = 0
def handler(_):
	global h
	h = 1

class TestCrawler(unittest.TestCase):

	def test_setting_handler_fails(self):
		crawler = ConcordanceCrawler("scrape")

		# test that you cannot set handler on ignored exception
		crawler.ignore_exception(OKException)
		self.assertRaises(Exception, crawler.set_exception_handler, OKException, None)

	def test_ignoring_exception_fails(self):
		crawler = ConcordanceCrawler("scrape")

		# you cannot ignore exception that already has handler
		crawler.set_exception_handler(EverythingIsOK, handler)
		self.assertRaises(Exception, crawler.ignore_exception, EverythingIsOK)

	def test_exception_handler_works(self):
		# test that handler for exception is really called
		global h,x
		x = 0
		crawler = ConcordanceCrawler("scrape")
		crawler.setup(get_raw_html=raise_error )
		crawler.set_exception_handler(EverythingIsOK, handler)
		c = zip(crawler.yield_concordances("scrape"), range(3))
		c = list(c)
		self.assertEqual(h,1)
		x = 0
		h = 0


	def test_ignoring_exceptions(self):
		crawler = ConcordanceCrawler("scrape")
		crawler.setup(get_raw_html=raise_error )
		crawler.ignore_exception(EverythingIsOK)
		c =  zip(crawler.yield_concordances("scrape"), range(3))
		try:
			list(c)
		except:
			assert False, 'test_ignoring_exceptions failed'





