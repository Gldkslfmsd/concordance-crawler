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
	reg = compile(r"^\s*$")
	splitreg = regex.compile(r"[\s-\p{P}\p{S}]")
#	splitreg = compile(r"[-\s -/:-@]")
	N = 3 # it will count 1, 2 and 3-grams
	spaces = " "*(N-2)

	def __init__(self, N=None):
		if N is not None:
			self.N = N

	def filter(self,word):
		return False

	def empty_freq(self):
		return [{} for _ in range(self.N)]

	def extract(self, line, freq=None):
		if freq is None:
			freq = self.empty_freq()
		for word in self.splitreg.split(line):
			if self.reg.match(word) or self.filter(word):
#				print("zahazuju",word)
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
	reg = compile(r".*[^a-zA-Z].*")
	def __init__(self, N=None):
		super(EnglishNGramsExtractor, self).__init__(N)

	def filter(self, word):
		return self.reg.match(word)

if __name__=="__main__":
	EnglishNGramsExtractor(10)
