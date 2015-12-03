# -*- coding: utf-8 -*-
import unittest
from ConcordanceCrawler.core.visitor import Visitor

class TestVisitor(unittest.TestCase):
	visitor = Visitor()

	def test_get_raw_html(self):
		raw_html = self.visitor.get_raw_html("http://www.airliners.net/aviation-forums/general_aviation/read.main/306713/")
		text = "do Lufthansa and United Airlines operate between their hubs please?"
		self.assertTrue(text in raw_html)

	def test_get_html_visible_text(self):
		raw_html = self.visitor.get_raw_html("https://en.wikipedia.org/wiki/Special:Random")

		visible = self.visitor.get_visible_text(raw_html)
		self.assertTrue("<br>" not in visible)
		self.assertTrue("<!--" not in visible)
		self.assertTrue("<html>" not in visible)
		self.assertTrue("Transclusion expansion time report" not in visible)
		self.assertTrue("window.RLQ.push" not in visible)

	# TODO
	def test_predict_format(self):
		pass

	def test_accept_format(self):
		pass

	def test_sentence_segmentation(self):
		text = """Hello,

		What do Lufthansa and United Airlines operate between their hubs please.
		What did they operate before applying code-share agreement? Bye! Ratatatata!
		au...
		"""
		sentences = self.visitor.sentence_segmentation(text)
		result = ['Hello,\n', '\n', 
		'\t\tWhat do Lufthansa and United Airlines operate between their hubs please.', 
		'\n', '\t\tWhat did they operate before applying code-share agreement?', 
		' Bye!', ' Ratatatata!', '\n','\t\tau.', '.', '.', '\n']
		for a,b in zip(sentences,result):
			self.assertEqual(a,b)

	# TODO
	def test_predict_language(self):
		lan = self.visitor.predict_language("hello world")
		self.assertEqual(lan, "eng")

	# TODO
	def test_accept_language(self):
		pass

	# TODO
	def test_norm_encoding(self):
		pass

	def test_concordances_filtering(self):
		# todo
		#self.assertTrue(self.visitor.concordance_filtering("večer","Dobrý večer, ..."))
		self.assertTrue(self.visitor.concordance_filtering("večer","Dobrý večer ..."))

	# todo: delete
	def test_split(self):
		s = 'hello world'
		self.assertEqual(s.split(), ['hello', 'world'])
		# check that s.split fails when the separator is not a string
		with self.assertRaises(TypeError):
			s.split(2)

	def test_visit_links(self):
		concs = self.visitor.visit_links([{"link":"https://cs.wikipedia.org/wiki/P%C5%99epaden%C3%AD_celnice_v_Habartic%C3%ADch"}],"akce")
		self.assertTrue(len(concs)>0)


if __name__=='__main__':
	unittest.main()
