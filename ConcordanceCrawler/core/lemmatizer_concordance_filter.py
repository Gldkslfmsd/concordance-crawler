from textblob import TextBlob, Word

def concordance_filtering(sentence, target, target_pos):
	blob = TextBlob(sentence)
	tags = blob.tags
	for w, t in tags:
		p = t.lower()[0]  # v for verb, n for noun, j for adjective
		pos = 'a' if p=='j' else pos
		if pos in target_pos:
			lemma = Word(w).lemmatize(pos)
			if lemma == target:
				return lemma
	return None
