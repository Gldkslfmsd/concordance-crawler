#!/usr/bin/env python3

"""Should have same functionality as frequencies.py, but I tried to do it
as fastest as possible. unsuccesfully in the end.
"""

from sys import argv

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

a = ord('a')
z = ord('z')
A = ord('A')
Z = ord('Z') 

def is_letter(l):
	return a <= ord(l) <= z or A <= ord(l) <= Z


N = 4
def cross(n):
	if n==0:
		for i in alphabet:
			yield (i,)	
	else:
		for i in alphabet:
			l = list(cross(n-1))
			for j in l:
				a = [i]+list(j)
				yield tuple(a)

def ngrams(n):
	for i in range(n):
		for j in cross(i):
			yield j
	
freq = {}
for n in range(N):
	freq.update( { l:0 for l in cross(n) } )

f = open(argv[1])
def add(i):
	if i in freq:
		freq[i]+=1
	else:
		freq[i] = 1
	return 1

def gram(line,n):
	return zip(*(line[k:] for k in range(n)))
	
all(map(
	lambda line: 
		all(map(
			lambda n:
				all(map(
						add, 
						(g for g in gram(line,n) if all(map(is_letter,g)))
				)), 
			range(N)
		)),
	f
))


l = [0 for _ in range(N)]
for g in ngrams(N):
#	if not g in freq:
#		freq[g] = 0
	l[len(g)-1] += freq[g]
print(l)

for n in range(N):
	for i in (k for k in freq.keys() if len(k)==n+1):
		if freq[i]:
			print("".join(i), freq[i]/l[n])
	
#print(freq)



#for i,v in enumerate(freq):
#	if freq[i]:
#		print(i,chr(i),v)
