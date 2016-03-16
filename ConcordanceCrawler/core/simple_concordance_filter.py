import re

'''This is a simple concordance filter, which uses only regular expression.
If a sentence contains target word in the same form as given on input,
a concordance is found.
'''

class ReConcordanceFilter:

	def __init__(self, target):
		self.target = target
		self.regex = re.compile(".*(\s|^)"+target+"(\s|$).*",flags=re.IGNORECASE)

	def process(self, sentence):
		return self.target if self.regex.match(sentence) else None


filters = {}
def regex_concordance_filtering(targets, sentence):
	global filters
	for target in targets:
		if not target in filters:
			filters[target] = ReConcordanceFilter(target)
		res = filters[target].process(sentence)
		if res:
			return res
	return None
	
