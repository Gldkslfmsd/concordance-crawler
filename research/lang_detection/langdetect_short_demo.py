# coding=utf-8
from langdetect import detect_langs as detect

from samples import *

for s in samples:
	print(detect(s))
