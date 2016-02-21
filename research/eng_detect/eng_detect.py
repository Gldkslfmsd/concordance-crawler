#!/usr/bin/python

from re import split
from freq import vector as english_vector
from ngrams_extractor import NGramsExtractor

class EngDetector:
	'''English Detector'''

	N = 4  # will use vector of 1,2,3-grams

	def __init__(self):
		self.extractor = NGramsExtractor(self.N)
		self.english_vector = english_vector.copy()
		for k in list(self.english_vector.keys()):
			if self.english_vector[k] < 3:
				del self.english_vector[k]
		self.english_vector = self.transform_to_ratio(self.english_vector)

	def transform_to_ratio(self, vector):
		for k in list(vector.keys()):
			if len(k)!=3:
				del vector[k]
		counts = [0 for _ in range(self.N)]
		for g in vector:
			counts[len(g)-1] += vector[g]
		for g in vector:
			vector[g] = vector[g] / counts[len(g)-1] 
		return vector

	def get_vector(self, text):
		freq = self.extractor.extract(text)
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

def test():
	det = EngDetector()
	import english_samples
	eng = []
	for s in english_samples.samples:
		eng.append(det.detect(s))
	print("mean:",sum(eng)/len(eng))

	print()
	import nonenglish_samples
	neng = []
	for s in nonenglish_samples.samples:
#		print(s[:20])
		neng.append(det.detect(s))
	print("mean:",sum(neng)/len(neng))


if __name__ == '__main__':
	det = EngDetector()

	test()



