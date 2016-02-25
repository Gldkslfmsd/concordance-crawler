#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''EngDetector gets a text and is able to detect, whether the text is in
English or not. It creates a vector of 1,2,3-gram frequencies and then
counts cosine similarity to the vector of 1,2,3-grams in English Wikipedia.
I call this cosine similarity `englishness`.

Method is_english(text) returns True/False, it should have TODO accuracy.'''

from re import split
from freq import ngrams
from thresholds import thresholds
from ngrams_extractor import NGramsExtractor

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
			print(sim, threshold)
			return False
		else:
			return True
		
import nonenglish_samples
import english_samples
debug = False
def test():
	det = EngDetector()
	eng = []
	for s in english_samples.samples:
		eng.append(det.englishness(s))
	if debug: 
		print("mean:",sum(eng)/(1.0*len(eng)))
		print()
	neng = []
	for s in nonenglish_samples.samples:
		#print(s[:20])
		neng.append(det.englishness(s))
	print("mean:",sum(neng)/(1.0*len(neng)))

def prepare_samples(slen,neng=nonenglish_samples.samples):
	nengall = " ".join(neng)
	engall = " ".join(english_samples.samples)
	sam = {
		"neng": [ nengall[i:i+slen] for i in range(0,len(nengall),slen) ],
		"eng": [ engall[i:i+slen] for i in range(0,len(engall),slen) ]
	}
	for k in list(sam.keys()):
		# cut the number of samples, because otherwise it's too slow
		sam[k] = sam[k][:300]
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
				det.englishness(s)
			)
	s = similarities
	print("neng mean",sum(s["neng"])/(1.0*len(s["neng"])))
	print("eng mean",sum(s["eng"])/(1.0*len(s["eng"])))
	return s

def do_big_test(samplelen):
	samples = prepare_samples(samplelen)
	sim = big_test(samples)
	similarities_to_file(sim)

def germanic_samples():
	from samples import germanic_samples as s
	texts = []
	for l, t in s:
		texts.extend(t)
	return texts

def gen_thresholds():
	lens = [10, 20, 30, 40, 
		50, 60, 70, 80, 90, 100,
		150, 200, 300, 400, 500, 1000, 1500, 2000, 5000]
	foreign_texts = germanic_samples()
	f = open("thresholds.py", "w")
	
	f.write("""'''Thresholds for EngDetector. Generated by eng_englishness.py,
(by function gen_threshold), can be changed manually. 

Threshold for "englishness" will be chosen by lenght of input text, because
the longer text, the better it fits to the vectors of frequencies of 1,2,3-grams in whole
English Wikipedia.

In comments are means similarities to English-Wikipedia vector of some
English and Non-English samples with given length.
'''\n\n\n""")

	f.write("thresholds = {\n")
	end = False
	try:
		for l in lens:
			sam = prepare_samples(l, neng=foreign_texts)
			print("length of samples:",l)
			sim = big_test(sam)
			nengmean = sum(sim["neng"])/(1.0*len(sim["neng"]))
			engmean = sum(sim["eng"])/(1.0*len(sim["eng"]))
			# threshold will be set as a center of interval between nengmean and
			# engmean, but you can change it manually in thresholds.py
			center = (nengmean+engmean)/2.0
			f.write(str(l)+": ")
			f.write(str(center) + ", # ")
			f.write("nengmean: "+str(nengmean)+" ")
			f.write("engmean: "+str(engmean)+" \n")
		end = True
	finally:
		f.write("}\n")
		if end:
			f.write("# Thresholds were generated correctly.\n")
		else:
			f.write("# Threshold generation was interrupted, the values can be incorrect!!!")
		f.close()
	

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

def test_detector():
	det = EngDetector()
	texts = ["Já mám práci rád.","Můžu se na ni dívat celý den.",
	"Bydlím v New Yorku.", 
	"Je ve Washingtonu DC.",  # example of sentence, that is considered English, but is in Czech


	"What's the difference between leaves and car?",
	"Is this text in English?", "Hello! Who's there?",
	"My hoovercraft is full of eels",
	"something "*5000]
	for t in texts:
		print(det.is_english(t))



if __name__ == '__main__':
	gen_thresholds()
#	test_languages(100)
#	test_detector()


