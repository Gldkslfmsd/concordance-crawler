# encoding=utf-8
import unittest
from ConcordanceCrawler.app.output_formatter import JsonFormatter

import six
if six.PY2:
	from simplejson import dumps
else:
	from json import dumps



class TestFormatter(unittest.TestCase):

	def test_json(self):

		f = open("x.json","w")
		jf = JsonFormatter(f)
		jf.output([{'a':'b'}])
		jf.close()
		f = open("x.json","r")
		correct = '''[
    [
        {
            "a": "b"
        }
    ]
]
'''
		self.assertTrue(f.read()==correct)
		f.close()

	# TODO
	def test_xml(self):
		pass

if __name__=='__main__':
	unittest.main()
