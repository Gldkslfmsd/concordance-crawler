#!/usr/bin/env python3

from re import split
from freq import ngrams
from ngrams_extractor import NGramsExtractor

class EngDetector:
	'''English Detector'''

	N = 3  # will use vector of 1,2,3-grams

	def __init__(self):
		self.extractor = NGramsExtractor(self.N)
		self.ngrams = ngrams[:self.N]
		list(map(self.transform_to_ratio, self.ngrams))

	def transform_to_ratio(self, vector):
		counts = [0 for _ in range(self.N)]
		for g in vector:
			counts[len(g)-1] += vector[g]
		for g in vector:
			vector[g] = vector[g] / counts[len(g)-1] 
		return vector

	def get_vectors(self, text):
		freq = self.extractor.extract(text)
		return list(map(self.transform_to_ratio, freq))

	def magnitude(self, vector):
		return sum(vector[k]**2 for k in vector.keys()) ** (1/2)

	def cosine_similarity(self, A, B):
		keys = set(A.keys()).intersection(B.keys())
		sim = sum(A[k]*B[k] for k in keys)
		return sim / (self.magnitude(A)*self.magnitude(B))

	def detect(self, text):
		vec = self.get_vectors(text)
		sim = []
		for v,ng in zip(vec, self.ngrams):
			csim = self.cosine_similarity(v, ng)
			sim.append(csim)
			print(csim)
		print("mean from 1,2,3-grams:",sum(sim)/len(sim))
		return sum(sim)/len(sim)

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
		print(s[:20])
		neng.append(det.detect(s))
	print("mean:",sum(neng)/len(neng))


if __name__ == '__main__':
	test()



