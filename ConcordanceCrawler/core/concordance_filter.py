import re

class ConcordanceFilter:

	def __init__(self, target):
		self.regex = re.compile(".*(\s|^)"+target+"(\s|$).*",flags=re.IGNORECASE)

	def process(self, sentence):
		return self.regex.match(sentence)

