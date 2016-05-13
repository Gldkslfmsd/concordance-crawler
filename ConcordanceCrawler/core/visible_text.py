import six
from bs4 import BeautifulSoup, SoupStrainer
import re

class VisibleTextParser:

	format_predictor = None

	def __init__(self):
		self.format_predictor = FormatPredictor()

	@staticmethod
	def _visible(element):
		if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
			return False
		if six.PY2:
			text = element.encode('utf-8')
		else:
			text = str(element)
		if re.match('<!--.*-->', text):
			return False
		return True

	def get_visible_text(self,html,format=None):
		'''Gets raw html, returns its plain text (without marks) that is visible by
		humans.
		'''
		# we delete html comments
		html = re.sub('<!--([^-]|-[^-]|--[^>])*-->',"",html)

		# Taken from here: http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
		soup = BeautifulSoup(html, "lxml")

		text = soup.findAll(text=True)
		visible_texts = "".join(filter(VisibleTextParser._visible, text))

		return visible_texts



class FormatPredictor():

	def predict_format(self,rawhtml,httpheader=None):
		# use just this strings, not constants, that would be too complicated
		formats = ["html", "doc", "pdf", "ppt", "odt", "unknown"]
		return "unknown"

class FormatFilter():
	def accept_format(self,format):
		return True



if __name__=='__main__':
	vp = VisibleTextParser()
	import requests
	import sys
	doc = open(sys.argv[1], "r").read()
	print(sys.argv)
	vis = vp.get_visible_text(doc)
	f = open("visible", "w")
	f.write(vis)
	f.close()

	"""
	path = "ConcordanceCrawler/core/viceroy.html"
	#path = "viceroy.html"
	f = open(path,'r')
	t = f.read()
	f.close()


	path2 = "https://en.wikipedia.org/wiki/Viceroy_of_Liangguang"
#	t = requests.get(path2)
	x = vp.get_visible_text(t)

	print(x)
	"""
	
