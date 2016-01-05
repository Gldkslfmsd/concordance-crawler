# coding=utf-8
from cheap_nltk_ld import is_english as detect

from samples import *

for s in samples:
	print(detect(s))
