from re import split, sub, compile


a = ord('a')
z = ord('z')
A = ord('A')
Z = ord('Z') 

def is_letter(l):
	return a <= ord(l) <= z or A <= ord(l) <= Z
def gram(t,n):
		return zip(*(t[k:] for k in range(n)))



class NGramsExtractor:
# TODO: in english vector there are also words containing Nonenglish letters
# ^.*[^a-zA-Z].*$
	reg = compile(r"^\s*$")
	splitreg = compile("[\s-]")
	N = 4 # it will count 1, 2 and 3-grams
	spaces = " "*(N-2)

	def __init__(self, N=None):
		if N is not None:
			self.N = N

	def extract(self, line, freq=None):
		if freq is None:
			freq = {}
		for word in self.splitreg.split(line):
			if self.reg.match(word):
				continue
			word = self.spaces+word+self.spaces
			for n in range(self.N):
				for g in gram(word, n):
					s = "".join(g)
					if not s in freq:
						freq[s] = 1
					else:
						freq[s] += 1

		return freq

