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
#			# TODO
#			#self.assertEqual(a,b)
#			pass

	# TODO -- better examples
	def test_language_filter(self):
		x = self.visitor.language_filter("""hello world, how are you? who's
		there? Is this text in English?""")
		print(x)
		self.assertTrue(x)

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
		concs = self.visitor.visit_links([{"link":"https://en.wikipedia.org/wiki/Lexicographically_minimal_string_rotation"}],"would")
		self.assertTrue(len(concs)>0)


if __name__=='__main__':
	unittest.main()
