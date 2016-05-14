import re

'''This is a simple concordance filter, which uses only regular expression.
If a sentence contains target word in the same form as given on input,
a concordance is found.

Regex matching a sentence containing given word is compiled only once and 
saved to `filters` global dictionary.
'''

class ReConcordanceFilter:

	def __init__(self, target):
		self.target = target
		#self.regex = re.compile(r"(\s|^)("+re.escape(target)+r")(\s|$|[-\]\[\.?!,:'\"/+*()\{\}<>#&@~=])",flags=re.IGNORECASE)
		
		self.regex = re.compile(r"(\s|^)(" + re.escape(target) + r")(\W|$)",
		flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)

	def process(self, sentence):
		m = self.regex.search(sentence)
		if m is None:
			return None
		return self.target, m.start(2), m.end(2)


filters = {}
def regex_concordance_filtering(sentence, targets):
	global filters
	for target in targets:
		if not target in filters:
			filters[target] = ReConcordanceFilter(target)
		res = filters[target].process(sentence)
		if res is not None:
			return res
	return None
	

if __name__ == "__main__":
	res = regex_concordance_filtering("s ConcordanceCrawler is a tool for automatic "
	"concordance extraction from the Internet.",["is","a"])
	print(res)
