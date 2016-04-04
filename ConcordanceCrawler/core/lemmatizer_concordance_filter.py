from textblob import TextBlob, Word
import re

def lemmatizing_concordance_filtering(sentence, target, target_pos):
	target = target[0]
	blob = TextBlob(sentence)
	for w, t in blob.tags:
		p = t.lower()[0]  # v for verb, n for noun, j for adjective
		if p == 'j':
			lpos = pos = 'a'
		if p in ['v', 'n', 'j']:
			lpos = pos = p
		else:
			pos = 'x'  # any indeclinable part of speech
			lpos = 'r'  # adverb for lemmatize (lemmatize should remain unchanged)
		if pos in target_pos:
			lemma = Word(w).lemmatize(pos)
			if lemma == target:
				m = re.search(w,sentence)
				return lemma, m.start(0), m.end(0)
	return None

if __name__ == "__main__":
	res = lemmatizing_concordance_filtering("We were flying from PRG to NY.",["fly"], "v")
	print(res)
	pass
