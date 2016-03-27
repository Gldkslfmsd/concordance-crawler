import chardet
import os
import time
html = [ f for f in os.listdir("../../kodovani_nedele/") if f.endswith(".html") ]
for n in html:
	with open("../../kodovani_nedele/"+n,"rb") as f:
		rawdata = f.read()
		s = time.time()
		v = chardet.detect(rawdata)
		e = time.time()
		print(n, v, e-s)
