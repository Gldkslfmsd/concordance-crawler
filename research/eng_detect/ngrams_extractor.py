from re import split, sub, compile
import regex

a = ord('a')
z = ord('z')
A = ord('A')
Z = ord('Z') 

def is_letter(l):
	return a <= ord(l) <= z or A <= ord(l) <= Z
def gram(t,n):
		return zip(*(t[k:] for k in range(n)))



class NGramsExtractor(object):
	reg = regex.compile(r"^\s*$")
	splitreg = compile("[\s-]")
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
			word = self.spaces+word.lower()+self.spaces
			for n in range(self.N):
				for g in gram(word, n):
					s = "".join(g)
					if not s in freq:
						freq[n-1][s] = 1
					else:
						freq[n-1][s] += 1
		return freq

class EnglishNGramsExtractor(NGramsExtractor):
	reg = regex.compile(r".*[^a-zA-Z].*")

	def __init__(self, N=None):
		super(EnglishNGramsExtractor, self).__init__(N)

	def filter(self, word):
		return self.reg.match(word)

if __name__=="__main__":
	EnglishNGramsExtractor(10)
