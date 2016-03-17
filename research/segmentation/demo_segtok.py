
from segtok.segmenter import split_multi
text = open("abbrev._text","r").read()
sentences = split_multi(text)

import results
results.print_results(sentences)

#for i in sentences:
#	print((i,))


