import re

class ConcordanceFilter:

	def __init__(self, target):
		self.regex = re.compile(".*(\s|^)"+target+"(\s|$).*",flags=re.IGNORECASE)

	def process(self, sentence):
		return True if self.regex.match(sentence) else False

filters = {}
def concordance_filtering(target, sentence):
	global filters
	if not target in filters:
		filters[target] = ConcordanceFilter(target)
	return filters[target].process(sentence)
	
