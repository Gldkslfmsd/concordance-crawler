#!/usr/bin/env python3

"""usage: ./frequencies.py files to process as args [...]

-- counts frequencies of {1,2,3}-grams in textfiles given as cmd args
-- ignores words that contain non-English letters (because they are
probably not in English)
-- processes files concurrently, it uses multiprocessing.Pool

"""

from multiprocessing import Pool, cpu_count
from sys import argv
from ngrams_extractor import NGramsExtractor

N = 4

def process_files(files):
	freq = {}
	extractor = NGramsExtractor(N)
	for f in map(open, files):
		for line in f:
			extractor.extract(line, freq)
		f.close()
	return freq

pool = Pool()
files = argv[1:]
chunked = [files[k::cpu_count()] for k in range(cpu_count())]
freqs = pool.map(process_files, chunked)

def join_freqs(freqs):
	f = freqs[0]
	for i in freqs[1:]:
		for k in i:
			if k in f:
				f[k] += i[k]
			else:
				f[k] = i[k]
	return f

freq = join_freqs(freqs)

print("vector = {")
for i in freq:
	print('"'+"".join(i)+'": ', freq[i],",",sep="")
print("}")
