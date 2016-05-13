#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''EngDetector gets a text and is able to detect, whether the text is in
English or not. It creates a vector of 1,2,3-gram frequencies and then
counts cosine similarity to the vector of 1,2,3-grams in English Wikipedia.
I call this cosine similarity `englishness`.

Method is_english(text) returns True/False, it should have TODO accuracy.'''

from re import split
from ConcordanceCrawler.core.eng_detect.freq import ngrams
from ConcordanceCrawler.core.eng_detect.thresholds import thresholds
from ConcordanceCrawler.core.eng_detect.ngrams_extractor import NGramsExtractor

class EngDetector:
	'''English Detector'''

	N = 3  # will use vector of 1,2,3-grams

	def __init__(self):
		self.extractor = NGramsExtractor(self.N)
		self.ngrams = [g.copy() for g in ngrams[:self.N]]
		list(map(self.frequency_filter, self.ngrams))
		list(map(self.transform_to_ratio, self.ngrams))

		self.thresholds = thresholds.copy()  # avoid changing it in future
		self.threshold_levels = sorted(list(self.thresholds.keys()))
	
	def frequency_filter(self, vector, threshold=100):
		'''vector: dict, e.g. { "ahb":10, "bžf":1 }
		removes keys and values, if value < threshold (so 'bžf' will be deleted)

		Used to exclude "noise" from English-Wikipedia n-grams frequencies
		vector. N-grams that occur less then threshold-times in 5 GB of English
		text are considered "noise".
		'''
		for k in list(vector.keys()):
			if vector[k] < threshold:
				del vector[k]

	def transform_to_ratio(self, vector):
		'''gets a histogram of occurences of n-grams in given text, transforms
		it to ratio of n-grams'''
		counts = 0
		for g in vector:
			counts += vector[g]
		for g in vector:
			vector[g] = vector[g] / (1.0*counts)
		return vector

	def get_vectors(self, text):
		'''returns: a list containing N vectors, a frequencies of 1,2,3...N
		grams in text'''
		freq = self.extractor.extract(text)
		return list(map(self.transform_to_ratio, freq))

	def magnitude(self, vector):
		return sum(vector[k]**2 for k in vector.keys()) ** (0.5)

	def cosine_similarity(self, A, B):
		if not A and not B:
			return 1
		if not A:
			return 0
		if not B:
			return 0
		keys = set(A.keys()).intersection(B.keys())
		sim = sum(A[k]*B[k] for k in keys)
		return sim / (1.0*self.magnitude(A)*self.magnitude(B))

	def get_threshold(self, text_len):
		'''finds the threshold of englishness for given length of text'''
		# this is a simple linear search in sorted set
		# can be changed to binary search
		level = self.threshold_levels[0]
		for l in self.threshold_levels:  # self.threshold_levels is sorted
			if text_len > l:
				level = l 
		return self.thresholds[level]

	def englishness(self, text):
		'''returns: a float number between 0 and 1, it's a similarity of text
		to really long English text'''
		vec = self.get_vectors(text)
		sim = []
		for v,ng in zip(vec, self.ngrams):
			csim = self.cosine_similarity(v, ng)
			sim.append(csim)
		mean = sum(sim)/(1.0*len(sim))
		return mean

	def is_english(self, text):
		'''returns: True/False, decides by threshold that was specified by
		training on English text and on texts in Germanic languages
		(the most relative and most similar languages to English)'''
		sim = self.englishness(text)
		threshold = self.get_threshold(len(text))
		if sim < threshold:
			return False
		else:
			return True
		
if __name__ == "__main__":
	import requests
	t = requests.get("http://lesbartavelles13.free.fr/IMAGE-ISO/ENGLISH6EME.iso").text
	print("staženo")
	
	d = EngDetector()

	print(d.englishness(t))

