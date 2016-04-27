from textblob import TextBlob, Word
import re

"""
TextBlob lemmatizer uses nltk.stem.WordNetLemmatizer(), which uses
following strings as part-of-speech values:

#{ Part-of-speech constants
ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
#}

Found on this link:
http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
"""

def tag_to_nltktag(tag):
	'''gets Penn Treebank POS tag (e.g. 'JJ', 'VBD', 'NN', ...), returns POS value
	for nltk.stem.WordNetlemmatizer (something from 'a', 's', 'r', 'n', 'v').
	'''

	t = tag.lower()[0]

	# it's verb, noun or adverb
	if t in ('v', 'n', 'r'):
		return t
	
	# it's adjective
	if t == "j":
		return "a"

	return None


def lemmatizing_concordance_filtering(sentence, target, pos_regex):
	'''args: 
		sentence -- string
		target -- a nonempty list containing target words, only the first is needed
		pos_regex -- compiled regex from standard re module

	returns:
		None if a sentence doesn't contain target word in desired form
		otherwise it returns a triple:
		target word lemma, start position, end postition of target in sentence
	'''
	target = target[0]
	blob = TextBlob(sentence)
	for w, t in blob.tags:
		if not pos_regex.match(t):
			continue
		nltk_pos = tag_to_nltktag(t)
		if nltk_pos is not None:
			lemma = Word(w).lemmatize(nltk_pos)
		else:  # POS is indeclinable, word is lemma
			lemma = w
		if lemma == target:
			m = re.search(w,sentence)
			return lemma, m.start(0), m.end(0)
	return None










# try whether it works 
if __name__ == "__main__":
	res = lemmatizing_concordance_filtering("We were flying from PRG to NY.",["fly"], re.compile("V.*"))

	print(res)
	res = lemmatizing_concordance_filtering("We were flying from PRG to NY.",["from"], re.compile("IN"))

	print(res)
	res = lemmatizing_concordance_filtering("We were flying from PRG to NY.",["to"], re.compile("TO"))

	print(res)
	res = lemmatizing_concordance_filtering("We bought beautiful blue balloons.",["balloon"], re.compile("N.*"))
	print(res)

	res = lemmatizing_concordance_filtering("We bought beautiful blue balloons.",["blue"], re.compile("N.*|J.*"))
	print(res)

	res = lemmatizing_concordance_filtering("We saw extremely nice blue balloons.",["extremely"], re.compile("R.*"))
	print(res)



