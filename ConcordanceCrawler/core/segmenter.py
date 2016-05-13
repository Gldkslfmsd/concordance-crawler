import re
import segtok.segmenter as segmenter
from ConcordanceCrawler.core.words_lower import words

reg = re.compile(r"[a-zA-Z]+\)?[.?!]\(?[a-zA-Z]+")

def sentence_segmentation(text):
	'''gets a text (string), returns list of sentences.
	
	Every item of a list should be one and only one whole sentence. (But in fact there are errors.)
	
	As a 'sentence' we define a sequence of words carrying one whole thought. E.g. the text on this line
	before "E.g." was one sentence. Compound sentence is also 'one sentence'. 'One sentence' is also a title 
	(beware, they are usually not ended by full stop) or a menu item.
	
	This function uses segmentation from `segtok` library, but it
	improves it by one additional rule. It tries to split also sentences that
	are not ended by dot and space, if the dot separates two existing English words present in dictionary.
	'''
	sentences = list(segmenter.split_multi(text))
	out_sentences = []
	for s in sentences:
		sen_words = s.split()
		current_sentence = []
		for w in sen_words:
			if not "http" in w and reg.match(w):
				a = re.split(r"(\)?[.!?:])\(?",w)
				if all(x.lower() in words or (x.lower().endswith("s") and x[:-1] in words) for x in a[:2:2]):
					current_sentence.append(a[0]+a[1])
					out_sentences.append(" ".join(current_sentence))
					current_sentence = ["".join(a[2:])]
				else:
					current_sentence.append(w)
			else:
				current_sentence.append(w)
		out_sentences.append(" ".join(current_sentence))
	return out_sentences


"""
# another unused segmenter versions
def raw_segtok_sentence_segmentation(text):
	return list(segmenter.split_multi(text))


def regex_sentence_segmentation(text):
	# NOTE: ... (three dots) get lost, but that would be too complicated

	# cut text to list: [ sentence, delimiter, sentence, delimiter, ... ]
	# e.g. [ "Hello", "!", " How are you", "?", "I'm fine", "." ]
	chunks = re.split("([\n\.\?\!])", text)

	# join sentence and its terminal mark
	# -> [ "Hello!", " How are you?", "I'm fine." ]
	sentences = [x + y for x, y in zip(chunks[::2], chunks[1::2])]

	return sentences

"""



if __name__ == "__main__":
	sentences = [
		"""And that's it (who did it).How do you say...""",
		"""e as a manufacturing error at source.The affected batches (see Table 1)
		have been parallel-imported by five companies (see Table 2).A
		spokeswoman for the MHRA said that each """,
		""""View in contextSwords to Plowshares Honors Manatt at Veterans Day
		CelebrationManatt Named 'Pro Bono Partner of the Year' For Work With
		VeteransHaving read, I believe, all of Ron Paul's books, I can say
		without any hesitation that Swords in      to Plowshares is undoubtedly
		his most important and most personal book.No wisdom in war: former
		presidential candidate and Congressman Ron Paul goes in-depth, using
		both moral and economic reasons, about why America should only go to war
		to defend itselfCircuit C      ourt of Appeals reversed the sabotage
		convictions of three Plowshares protesters --Holy Child Jesus Sr.Court
		reverses convictionsFurthermore it is about GUIDES option drags and
		plowshares adapted snow removal from synthetic football pitch, extended
		service agreem      ent, long foregoing, running track and stE[sup.The
		mission encompasses removal gammalt synthetic football, necessary in
		assassinating surface and installation of a new synthetic football
		cover.",""",
		"""However, the annex goes on to say that it
		is improbable that a procedure could be satisfactorily validated for
		starting materials for use in parenteral products.Unless variations are
		submitted for all affected products, the registered meth      od for
		confirming identity should be performed.""",
		"It was a very first.How do you do?",
		"""i hit the button to download now, it said my sd card was safe to
		remove, and thats it. looked in settings and still running 2.1 and
		system is up to date.""",
		"""But you should never take more unless a doctor says
		so.Category:(children &amp; adults)Tolerable upper intake levels (ul)
		ofVitamin e (alpha-tocopherol)In milligrams (mg) and international units
		(iu)1-3 years200 mg/day (300 iu)4-8 years300       mg/day (450 iu)9-13
		years600 mg/day (900 iu)14-18 years800 mg/day (1, 200 iu)19 years and
		up1, 000 mg/day (1, 500 iu) Good sources of vitamin e include:Vegetable
		oilsGreen leafy vegetables, like spinachFortified cereals and other
		foodsEggsNutsRisks of taking vit      amin e:The risks and benefits of
		taking vitamin e are still unclear.""",
		]
	for s in sentences:
		print(sentence_segmentation(s))
