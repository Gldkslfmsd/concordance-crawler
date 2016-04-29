# -*- coding: utf-8 -*-
from re import split, sub, compile
import regex

a = ord('a')
z = ord('z')
A = ord('A')
Z = ord('Z') 

def is_letter(l):
	return a <= ord(l) <= z or A <= ord(l) <= Z
def gram(t,n):
	"""t: word, n: lenght of gram (1 for 1-gram etc)
	"""
	return zip(*(t[k:] for k in range(n)))

class NGramsExtractor(object):
	"""Extracts a vector (or histogram) of 1, 2,... and N-grams from given texts.
	Words are separated by spaces or other symbols than letters, then
	wrapped by spaces, converted to lowercase and cuted to n-ples (single,
	double, triple, ... ) of chars.

	For example, word "hello" is splited to 1-grams this way:
	['h', 'e', 'l', 'l', 'o'],

	2-grams:
	[' h', 'he', 'el', 'll', 'lo', 'o ']
	
	3-grams:
	['  h', ' he', 'hel', 'ell', 'llo', 'lo ', 'o  ']
	"""
	
	# should match words composed from spaces or containing any non letter
	# symbol (e.g. "PRG1", "Y2K", "O2" ), because they are probably not words,
	# but some random codes
	excludereg = regex.compile(r"^\s*$|^.*[^\p{L}].*$")

	# we will split words by punctuation and spaces
	splitreg = regex.compile(r"[\s-\p{P}\p{S}]")
	N = 3 # it will count 1, 2 and 3-grams
	spaces = " "*(N-2)

	def __init__(self, N=None):
		'''N: it will extract 1,2,3... and N-grams. Default value for N is 3.'''
		if N is not None:
			self.N = N

	def filter(self,word):
		'''If it returns True, word will be filtered. Can be overriden in
		descendant class.'''
		return False

	def empty_freq(self):
		'''Returns empty vector of frequencies of 1,2,3...N-grams.
		
		It is a list of dicts, on i-th index is a histogram of
		(i-1)-grams. Histogram is a dict with grams as keys and number of
		occurences as values.
		'''
		return [{} for _ in range(self.N)]

	def extract(self, line, freq=None):
		'''
		line: input text
		freq: if None, create a new vector, otherwise the n-grams will be added
		to freq. That can be used to reduce time complexity, if you call this
		method multiple-times and then want to merge its results to one vector. 

		freq is a list of dicts, on i-th index is a histogram of
		(i-1)-grams. Histogram is a dict with grams as keys and number of
		occurences as values.

		returns: histogram of frequencies of 1,2,3...N-grams in line.

		Example: 
		>>> NGramsExtractor().extract("Hello.")
		[{'h': 1, 'e': 1, 'l': 2, 'o': 1}, {'el': 1, 'lo': 1, ' h': 1, 'o ': 1,
		'll': 1, 'he': 1}, {'lo ': 1, 'o  ': 1, 'ell': 1, '  h': 1, 'llo': 1,
		'hel': 1, ' he': 1}]
		'''
		if freq is None:
			freq = self.empty_freq()
		for word in self.splitreg.split(line):
			if self.excludereg.match(word) or self.filter(word):
				continue
			word = word.lower()
			for n in range(self.N):
				for g in gram(" "*n+word+" "*n, n+1):
					s = "".join(g)
					assert len(s)==n+1
					if not s in freq[n]:
						freq[n][s] = 1
					else:
						freq[n][s] += 1
		return freq

class EnglishNGramsExtractor(NGramsExtractor):
	"""EnglishNGramsExtractor is the same as NGramsExtractor, but filters
	words containing any Non-English letter or letter with diacritics (e.g.
	'Holešovice', 'résumé'), because they will be probably a loanwords or
	a words from some other language.""" 
	reg = compile(r".*[^a-zA-Z].*")
	def __init__(self, N=None):
		super(EnglishNGramsExtractor, self).__init__(N)

	def filter(self, word):
		return self.reg.match(word)

if __name__=="__main__":
	#def example():
	#	ext = NGramsExtractor()
	#	print(ext.extract("Hello."))

	#print(EnglishNGramsExtractor(10).extract("čau"))
	#print(EnglishNGramsExtractor(5).extract("č-au"))
	#example()


	import requests
	t = requests.get("http://lesbartavelles13.free.fr/IMAGE-ISO/ENGLISH6EME.iso").text

#	t = t[:100000]
	ext = NGramsExtractor()
	print(len(t))
	f = ext.extract(t)
	print(sum(len(e.keys()) for e in f))
	print(f)
