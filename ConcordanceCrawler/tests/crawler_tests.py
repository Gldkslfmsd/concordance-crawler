import unittest

from ConcordanceCrawler.core.logging_crawler import *

problem = {
"url": "http://www.spearfuneralhome.net/displayfuneral.php?item=205&letter=", 
"date": "2016-03-15 20:29:14.640150", 
"concordance": "And Athena,   goddess of wisdom to store the fate of mankind and quietly on the bottom of this box positive things \"hope\" too little time for fly as well as, positioned the [url=http://www.filsfils.com/]http://www.filsfils.com/[/url] \rones own style.", 
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
