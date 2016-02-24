#!/usr/bin/env python3

from re import split
from freq import ngrams
from ngrams_extractor import NGramsExtractor

class EngDetector:
	'''English Detector'''

	N = 3  # will use vector of 1,2,3-grams

	def __init__(self):
		self.extractor = NGramsExtractor(self.N)
		self.ngrams = [g.copy() for g in ngrams[:self.N]]
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
		if not A and not B:
			return 1
		if not A:
			return 0
		if not B:
			return 0
		keys = set(A.keys()).intersection(B.keys())
		sim = sum(A[k]*B[k] for k in keys)
		return sim / (self.magnitude(A)*self.magnitude(B))

	def detect(self, text):
		vec = self.get_vectors(text)
		sim = []
		for v,ng in zip(vec, self.ngrams):
			csim = self.cosine_similarity(v, ng)
	#		if csim==0: 
	#			print((text,))
			sim.append(csim)
		mean = sum(sim)/len(sim)
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

def prepare_samples(slen,neng=nonenglish_samples.samples):
	nengall = " ".join(neng)
	engall = " ".join(english_samples.samples)
	sam = {
		"neng": [ nengall[i:i+slen] for i in range(0,len(nengall),slen) ],
		"eng": [ engall[i:i+slen] for i in range(0,len(engall),slen) ]
	}
	return sam

def similarities_to_file(sims):
	f = open("similarities.py","w")
	f.write("similarities = ")
	f.write(str(sims))
	f.close()
	
def big_test(samples):
	det = EngDetector()
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
	return s

def do_big_test(samplelen):
	samples = prepare_samples(samplelen)
	sim = big_test(samples)
	similarities_to_file(sim)

def test_languages(samplelen):
	from samples import lang_samples
	res = {}
	for language, texts in lang_samples:
		sam = prepare_samples(samplelen, texts)
		print(language)
		sim = big_test(sam)
		res["eng"] = sim["eng"]
		res[language] = sim["neng"]

	similarities_to_file(res)
	



if __name__ == '__main__':
	test_languages(50)


