#!/usr/bin/env python3

"""usage: ./frequencies.py files to process as args [...]

-- counts frequencies of {1,2,3}-grams in textfiles given as cmd args
-- ignores words that contain non-English letters (because they are
probably not in English)
-- processes files concurrently, it uses multiprocessing.Pool

"""

from multiprocessing import Pool, cpu_count
from sys import argv
from re import split, sub, compile

#alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

a = ord('a')
z = ord('z')
A = ord('A')
Z = ord('Z') 

def is_letter(l):
	return a <= ord(l) <= z or A <= ord(l) <= Z
def gram(t,n):
		return zip(*(t[k:] for k in range(n)))

reg = compile(r"^.*[^a-zA-Z].*$|^\s*$")
splitreg = compile("[\s-]")
N = 4 # it will count 1, 2 and 3-grams

spaces = " "*(N-2)

def process_files(files):
	freq = {}
	for f in map(open, files):
		counts = [0 for n in range(N)]	
		for line in f:
			for word in splitreg.split(line):
				if reg.match(word):
#					print("filtruju!",word,"!",sep="")
					continue
				word = spaces+word+spaces
#				print("!",word,"!",sep="")
				for n in range(N):
					for g in gram(word, n):
						if not g in freq:
							freq[g] = 1
						else:
							freq[g] += 1
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
