"""Few tests of EngDetect that should be run and evaluated manually"""

import english_samples
from prepare_thresholds import *
debug = False

def test():
	det = EngDetector()
	eng = []
	for s in english_samples.samples:
		eng.append(det.englishness(s))
	if debug: 
		print("mean:",sum(eng)/(1.0*len(eng)))
		print()
	neng = []
	for s in nonenglish_samples.samples:
		#print(s[:20])
		neng.append(det.englishness(s))
	print("mean:",sum(neng)/(1.0*len(neng)))

def similarities_to_file(sims):
	f = open("similarities.py","w")
	f.write("similarities = ")
	f.write(str(sims))
	f.close()
	
def test_languages(samplelen):
	'''counts englishness of some samples in Germanic and Romanic languages in package
	`samples`. 
	Then it creates similarities.py, so you can run plots.py and watch boxplots
	and ROC curve'''
	from samples import lang_samples
	res = {}
	for language, texts in lang_samples:
		sam = prepare_samples(samplelen, texts)
		print(language)
		sim = big_test(sam)
		res["English"] = sim["eng"]
		res[language] = sim["neng"]

	similarities_to_file(res)

def test_detector():
	det = EngDetector()
	texts = ["Já mám práci rád.","Můžu se na ni dívat celý den.",
	"Bydlím v New Yorku.", 
	"Je ve Washingtonu DC.",  # example of sentence, that is considered English, but is in Czech


	"What's the difference between leaves and car?",
	"Is this text in English?", "Hello! Who's there?",
	"My hoovercraft is full of eels",
	"something "*5000]
	for t in texts:
		print(t[:80],det.is_english(t))

def do_big_test(samplelen):
	'''counts englishness of texts in english_samples.py and
	non_english_samples.py, then rewrites simialrities.py -> you can see plots'''
	samples = prepare_samples(samplelen)
	sim = big_test(samples)
	similarities_to_file(sim)

def compare_with_langdetect():
	print("eng_detect")
	test_detector()

	import langdetect
	def langd_englishness(_,text):
		l = langdetect.detect_langs(text)
		if 'en' in l:
			return l['en']
		return 0

	def langd_is_english(_,text):
		if langd_englishness(_,text):
			return True
		return False

	EngDetector.englishness = langd_englishness
	EngDetector.is_english = langd_is_english

	print()
	print("langid")
	test_detector()


if __name__ == "__main__":
#	test()
	test_languages(500)
#	test_detector()
#	do_big_test(100)

	#compare_with_langdetect()
