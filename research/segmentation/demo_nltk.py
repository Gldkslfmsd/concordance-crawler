
from nltk.tokenize import sent_tokenize
text = open("abbrev._text","r").read()
sentences = sent_tokenize(text)

import results
results.print_results(sentences)
#for i in sentences:
#	print((i,))

