#!/usr/bin/env python3

"""Bazwords generators"""

import random
class RandomShortWords():
	"""Generates bazwords that look like 4 random letters"""
	letters = [ chr(a) for a in range(ord('a'),ord('z')+1) ]
	def __init__(self,seed = None):
		if seed:
			random.seed(seed)

	def get_bazword(self):
		baz = ""
		for i in range(4):
			baz += random.choice(self.letters)
		return baz

#TODO:
#class WikipediaRandomArticle
#class NormalWords
#class Numbers

if __name__ == "__main__":
	a = RandomShortWords()
	for i in range(10):
		x = a.get_bazword()

		print(x)
