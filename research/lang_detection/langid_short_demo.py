# coding=utf-8
from langid import classify as detect

from samples import *

for s in samples:
	print(detect(s))
