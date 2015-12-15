
import re

r = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s",re.MULTILINE)
text = open("abbrev._text","r").read()
sentences = r.split(text)

import results
results.print_results(sentences)

#for i in sentences:
#	print((i,))




