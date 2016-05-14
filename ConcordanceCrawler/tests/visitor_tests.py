# -*- coding: utf-8 -*-
import unittest
from ConcordanceCrawler.core.visitor import Visitor

class TestVisitor(unittest.TestCase):
	visitor = Visitor()

	def test_get_raw_html(self):
		raw_html, headers = self.visitor.get_raw_html("http://www.airliners.net/aviation-forums/general_aviation/read.main/306713/")
		text = "do Lufthansa and United Airlines operate between their hubs please?"
		self.assertTrue(text in raw_html)

	def test_get_html_visible_text(self):
		raw_html, _ = self.visitor.get_raw_html("https://en.wikipedia.org/wiki/Special:Random")

		visible = self.visitor.get_visible_text(raw_html)
		self.assertTrue("<br>" not in visible)
		self.assertTrue("<!--" not in visible)
		self.assertTrue("<html>" not in visible)
		self.assertTrue("Transclusion expansion time report" not in visible)
		self.assertTrue("window.RLQ.push" not in visible)

	def test_predict_format(self):
		pass

	def test_accept_format(self):
		pass

	def test_sentence_segmentation(self):
		text = """Hello,

		What do Lufthansa and United Airlines operate between their hubs please.
		What did they operate before applying code-share agreement? Bye! Ratatatata!
		au... 

		Call him etc. and do do Lufthansa and Dr. Gregory House M.D. operate between their hubs please.
		"""

		sentences = self.visitor.sentence_segmentation(text)

		right = ['Hello,', 'What do Lufthansa and United Airlines operate between their '
		'hubs please.', 'What did they operate before applying code-share '
		'agreement?', 'Bye!', 'Ratatatata!', 'au...', 'Call him etc. and do do '
		'Lufthansa and Dr. Gregory House M.D. operate between their hubs '
		'please.', '']

		for a,b in zip(sentences,right):
			self.assertEqual(a,b)

#	def test_czech_sentence_segmentation(self):
#		'''this will test czech sentence segmentation, which is currently not
#		finished yet
#		'''
#
#		# text to segment
#		text = """
#		Are you really JUDr. PhDr. MUDr. RNDr. Mgr. et Mgr., Bc. Henryk Lahola,
#		Th.D., DrSc., multi dr.h.c. or not? Tyto zkratky to neumí, to je blbý
#		s.r.o. Že? 
#		
#		Jedu z Praha hl.n. do U.S. vlakem 16.07.2015.
#		Jedu z Praha hl. n. do U. S. přes Čes. Bud. stopem 16.7. 2015.
#		Jedu z Praha hl. n. Českými drahami a.s. do U.S. stopem 16. 7. 2015.
#
#		"""
#		# right answers
#		right = [u'''Are you really JUDr. PhDr. MUDr. RNDr. Mgr. et Mgr., Bc. Henryk Lahola,
#		Th.D., DrSc., multi dr.h.c. or not?''',
#		u'''Tyto zkratky to neumí, to je blbý
#		s.r.o.''',
#		u'''Že? 
#		''',
#
#		u'Jedu z Praha hl.n. do U.S. vlakem 16.07.2015.',
#		u'Jedu z Praha hl. n. do U. S. přes Čes. Bud. stopem 16.7. 2015.',
#		u'Jedu z Praha hl. n. Českými drahami a.s. do U.S. stopem 16. 7. 2015.',
#		]
#		sentences = self.visitor.sentence_segmentation(text)
#		for a,b in zip(sentences,right):
#			#self.assertEqual(a,b)
#			pass

	def test_language_filter(self):
		x = self.visitor.language_filter("""hello world, how are you? who's
		there? Is this text in English?""")
		self.assertTrue(x)

		eng = ["https://en.wikipedia.org/wiki/Russian_language",
		"https://en.wikipedia.org/wiki/Main_Page",
		#"https://www.usa.gov/", 
		]
		for url in eng:
			html, _ = self.visitor.get_raw_html(url)
			t = self.visitor.get_visible_text(html)
			self.assertTrue(self.visitor.language_filter(t))

		neng = [
			"https://cs.wikipedia.org/wiki/Speci%C3%A1ln%C3%AD:N%C3%A1hodn%C3%A1_str%C3%A1nka",
			"https://pl.wikipedia.org/wiki/Specjalna:Losowa_strona",
			"https://it.wikipedia.org/wiki/Speciale:PaginaCasuale",
			"https://es.wikipedia.org/wiki/Especial:Aleatoria",
			]
		for url in neng:
			html, _ = self.visitor.get_raw_html(url)
			t = self.visitor.get_visible_text(html)
			self.assertFalse(self.visitor.language_filter(t))

	
	def test_concordances_filtering(self):
		self.assertTrue(self.visitor.concordance_filtering("Dobrý \n\nVečer", ["večer"]))
		self.assertTrue(self.visitor.concordance_filtering("Dobrý večer, ...", ["večer"]))
		self.assertTrue(self.visitor.concordance_filtering("Dobrý večer ...",["večer"]))
		self.assertTrue(self.visitor.concordance_filtering("Dobrý večer...",["večer"]))
		self.assertTrue(self.visitor.concordance_filtering("Dobrý večer!",["večer"]))
		self.assertTrue(self.visitor.concordance_filtering("Dobrý večer?sdfas",["večer"]))

	def test_visit_link(self):
		concs = self.visitor.concordances_from_link("https://en.wikipedia.org/wiki/President_of_the_United_States",["president", "presidents"])
		self.assertTrue(len(concs)>0)


	def test_norm_encoding(self):
		meta_utf = 'sdfas <meta charset="utf-8"'
		meta_UTF = 'sdfas <meta charset="UTF-8"'

		header_utf = 	{"Content-Type": "text/html; charset=UTF-8;"}
		header_ct_nothing = {"Content-Type": "text/html;"}
		header_iso = {"Content-Type": "text/html; charset=iso-8859-1;"}

		true = [
			(meta_utf, header_utf),
			(meta_UTF, header_utf),
			(meta_utf, header_ct_nothing),
			("sfdasdfsa charset=\"utf-8\"",header_utf),
			("sfdasdfsa charset=\"utf-8;sdfs \"",header_utf),
			("sfdasdfsa charset=\"utf-8;sdfs \"",header_ct_nothing),
			("sfdasdfsa charset=utf-8 ;sdfs \"",header_utf),
			("sfdasdfsa charset=utf-8 ;sdfs \"",header_ct_nothing),
			("sfdasdfsa charset='utf-8' ;sdfs \"",header_utf),
			("sfdasdfsa charset='utf-8' ;sdfs \"",header_ct_nothing),
			]

		false = [
			(meta_utf, {}),
			("sfdasdfsa fsdfasfdsa fdsfdasfdsa charset=sdfafdsafasfasf",header_utf),
			("sfdasdfsacharset=utf-16",header_utf),
			("sfdasdfsa charset=\"iso-8859-1\"",header_utf),
			("sfdasdfsa ",header_iso),
			("sfdasdfsa ",header_ct_nothing),
			(meta_utf, header_iso),
			]


		for a,b in true:
			x = self.visitor.norm_encoding(a, headers=b)
			self.assertIsNotNone(x)

		for a,b in false:
			x = self.visitor.norm_encoding(a, headers=b)
			self.assertIsNone(x)


if __name__=='__main__':
	unittest.main()
