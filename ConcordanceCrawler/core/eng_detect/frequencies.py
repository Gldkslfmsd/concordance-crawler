#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""usage: python frequencies.py files to process as args [...] > freq.py

-- counts frequencies of {1,2,3}-grams in textfiles given as cmd args
-- ignores words that contain non-English letters (because they are
probably not in English, but loanwords or citation of other language)
-- processes files concurrently, it uses multiprocessing.Pool
-- writes vector of frequencies used by EngDetect on stdout

"""

from multiprocessing import Pool, cpu_count
from sys import argv
from ngrams_extractor import EnglishNGramsExtractor

N = 3

def process_files(files):
	extractor = EnglishNGramsExtractor(N)
	freq = extractor.empty_freq()
	for f in map(open, files):
		for line in f:
			extractor.extract(line, freq)
		f.close()
	return freq

pool = Pool()
files = argv[1:]
chunked = [files[k::cpu_count()] for k in range(cpu_count())]
freqs = pool.map(process_files, chunked)

def join_dicts(A, B):
	for k in B.keys():
		if k in A.keys():
			A[k] += B[k]
		else:
			A[k] = B[k]
	return A

def join_freqs(freqs):
	f = freqs[0]
	for i in freqs[1:]:
		for a,b in zip(f,i):
			join_dicts(a,b)
	return f

freq = join_freqs(freqs)

print("ngrams =", freq)
