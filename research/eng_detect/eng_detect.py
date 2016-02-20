#!/usr/bin/python

from re import split

a = ord('a')
z = ord('z')
A = ord('A')
Z = ord('Z') 

def is_letter(l):
	return a <= ord(l) <= z or A <= ord(l) <= Z
def gram(t,n):
		return zip(*(t[k:] for k in range(n)))

class EngDetector:
	'''English Detector'''

	N = 4  # will use vector of 1,2,3-grams

	def __init__(self):
		f = open("freq","r")

		self.english_vector = {}
		for line in f:
			g, c = line.split()
			c = int(c)
#			if c<10: continue
			self.english_vector[g] = c
		f.close()
		self.english_vector = self.transform_to_ratio(self.english_vector)

	def transform_to_ratio(self, vector):
		counts = [0 for _ in range(self.N)]
		for g in vector:
			counts[len(g)-1] += vector[g]
		for g in vector:
			vector[g] = vector[g] / counts[len(g)-1] 
		return vector


	def get_vector(self, text):
		freq = {}
		for word in split("[\W\d]",text):
			for n in range(self.N):
				for g in gram(word, n):
					s = "".join(g)
					if not s in freq:
						freq[s] = 1
					else:
						freq[s] += 1
		return self.transform_to_ratio(freq)

	def magnitude(self, vector):
		return sum(vector[k]**2 for k in vector.keys()) ** (1/2)

	def cosine_similarity(self, A, B):
		keys = set(A.keys()).intersection(B.keys())
		sim = sum(A[k]*B[k] for k in keys)
		return sim / (self.magnitude(A)*self.magnitude(B))

	def detect(self, text):
		vec = self.get_vector(text)
		csim = self.cosine_similarity(vec, self.english_vector)
		print(csim)
		return csim
#		print(self.vector)

def test():
	det = EngDetector()
	import english_samples
	eng = []
	for s in english_samples.samples:
		eng.append(det.detect(s))
	print("průměr:",sum(eng)/len(eng))

	print()
	import nonenglish_samples
	neng = []
	for s in nonenglish_samples.samples:
		neng.append(det.detect(s))
	print("průměr:",sum(neng)/len(neng))




if __name__ == '__main__':
	det = EngDetector()
#	det.detect("ahoj štěňátko")#, 3-gramy a česko-německý slovník")

	test()



