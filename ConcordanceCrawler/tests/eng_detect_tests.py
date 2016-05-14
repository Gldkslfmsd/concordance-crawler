# -*- coding: utf-8 -*-
import unittest
import re
import regex

from ConcordanceCrawler.core.eng_detect.eng_detect import *

def dict_equals(A,B):
	Aitems = set(A.items()) 
	Bitems = set(B.items())
	return Aitems.issubset(Bitems) and Bitems.issubset(Aitems)

class TestEngDetector(unittest.TestCase):

	det = EngDetector()

	def test_thresholds(self):
		det = self.det
		self.assertIsNotNone(det.thresholds)
		self.assertNotEqual(det.thresholds, {})

	def test_transform_to_ratio(self):
		det = self.det
		for g in det.ngrams:
			self.assertTrue(1.0-10**(-6) <= sum(g.values()) <= 1.0+10**(-6))

	def test_eng_ngrams(self):
		ngrams = self.det.ngrams
		reg = re.compile(r"^[ a-z]+$")
		for i,g in enumerate(ngrams):
			for k,v in g.items():
				self.assertTrue(0 < v <= 1)
				self.assertTrue(i+1 == len(k))
				self.assertIsNotNone(reg.match(k))

	def test_ngrams(self,ngrams=None):
		if ngrams is None:
			return
		reg = regex.compile(r"^[ \p{L}]+$")
		for i,g in enumerate(ngrams):
			for k,v in g.items():
				self.assertTrue(0 < v)
				self.assertTrue(i+1 == len(k))
				self.assertIsNotNone(reg.match(k))

	def test_exclude_regex(self):
		match = ["Y2K", "2011", "xml2json", "@ový", "@![Đđ~\|€[]&@{!@#$%!",
		" "*10, "32010348321213223", ""]

		for w in match:
			self.assertIsNotNone(self.det.extractor.excludereg.match(w))

		notmatch = ["něcoíéščřéšě", "نظر", "normal"]
		for w in notmatch:
			self.assertIsNone(self.det.extractor.excludereg.match(w))

	def test_split_regex(self):
		text = "abc  \n\n\n de\tf-g--h@něco.com||500GKL"
		splitted = self.det.extractor.splitreg.split(text)
		correct = ['abc', '', '', '', '', '', 'de', 'f', 'g', '', 'h', 'něco',
		'com', '', '500GKL']
		for a,b in zip(splitted, correct):
			self.assertEqual(a,b)

	def test_extractor(self):

		test_cases = [
			(	"abcč", [{'a': 1, 'c': 1, 'č': 1, 'b': 1}, {'č ': 1, 'ab': 1, 'bc':
			1, 'cč': 1, ' a': 1}, {'abc': 1, 'č  ': 1, 'cč ': 1, '  a': 1, ' ab':
			1, 'bcč': 1}]),
			( "1", [{},{},{}]),
			( "12th street", [{'r': 1, 's': 1, 'e': 2, 't': 2}, {'tr': 1, 'ee': 1, 'et': 1, ' s':
			1, 't ': 1, 're': 1, 'st': 1}, {'eet': 1, '  s': 1, 'tre': 1, 'et ':
			1, 'str': 1, 't  ': 1, ' st': 1, 'ree': 1}]),
			("", [{},{},{}]),
		]
		
		ext = self.det.extractor
		for text, test_grams in test_cases:
			ext_grams = ext.extract(text)
			self.test_ngrams(ext_grams)
			self.assertTrue(all(map(dict_equals, ext_grams, test_grams)))

	def test_is_english(self):
		texts = ["""A true SSLContext object is not available. This prevents
		urllib3 from configuring SSL appropriately and may cause certain SSL
		connections to fail. For more information, see""",
		"""Gravitational waves: Tests begin for future space observatory""",
		"""this should be an english text""", 
		]

		for t in texts:
			self.assertTrue(self.det.is_english(t))

		texts = ["र्वी स्लाभिक भाषाय् दक", """географически и по числу носителей языка как
		родног""", """وه. دغه ژبه د مذهبی""", """ti. D1 blokují kamiony, D8 je
		uzavřena""", "ha"*10000]
		for t in texts:
			self.assertFalse(self.det.is_english(t))

