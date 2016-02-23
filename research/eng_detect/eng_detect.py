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
		list(map(self.frequency_filter, self.ngrams))
		list(map(self.transform_to_ratio, self.ngrams))
	
	def frequency_filter(self, vector, threshold=100):
		'''vector: dict, e.g. { "ahb":10, "bžf":1 }
		removes keys and values, if value < threshold (so 'bžf' will be deleted)
		'''
		for k in list(vector.keys()):
			if vector[k] < threshold:
				del vector[k]

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
	#		print(csim)

		weighted_mean = sum(s*(i+1) for s,i in zip(sim,range(3)))/6
		mean = sum(sim)/len(sim)
		two_grams = sim[2]

	#	print("mean from 1,2,3-grams:",sum(sim)/len(sim))
	#	print("wmean: ",res)
		return mean

import nonenglish_samples
import english_samples
debug = False
def test():
	det = EngDetector()
	eng = []
	for s in english_samples.samples:
		eng.append(det.detect(s))
	if debug: 
		print("mean:",sum(eng)/len(eng))
		print()
	neng = []
	for s in nonenglish_samples.samples:
		#print(s[:20])
		neng.append(det.detect(s))
	print("mean:",sum(neng)/len(neng))

def prepare_samples(slen):
	nengall = " ".join(nonenglish_samples.samples)
	engall = " ".join(english_samples.samples)
	sam = {
		"neng": [ nengall[i:i+slen] for i in range(0,len(nengall),slen) ],
		"eng": [ engall[i:i+slen] for i in range(0,len(engall),slen) ]
	}
	return sam

def try_plot(sims):
	f = open("similarities.py","w")
	f.write("similarities = ")
	f.write(str(sims))
	f.close()
	
def big_test(samplelen):
	det = EngDetector()
	samples = prepare_samples(samplelen)
	similarities = {
		"neng": [],
		"eng": [],
	}
	for p in ("neng", "eng"):
		for s in samples[p]:
			similarities[p].append(
				det.detect(s)
			)
	s = similarities
	print("neng mean",sum(s["neng"])/len(s["neng"]))
	print("eng mean",sum(s["eng"])/len(s["eng"]))
	try_plot(similarities)


def kotatko():
	d = EngDetector()
	v = d.detect("ubohé malé koťátko...")
	for k in v:
		print("' '".join(k.keys()))



if __name__ == '__main__':
	big_test(100)


