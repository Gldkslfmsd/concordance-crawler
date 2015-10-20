
import ConcordanceCrawler.core.urlrequest as urlreq

# TODO:
# all classes using Internet (e.g. Wikipedia bazword generators, visitor,
# crawling links) will inherit this class
class InternetUser:
	def get_raw_html(self, url):
		return urlreq.get_raw_html(url)
