# encoding=utf-8
import unittest
from ConcordanceCrawler.app.output_formatter import JsonFormatter, XmlFormatter

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

	def test_xml(self):
		f = open("x.xml","w")
		jf = XmlFormatter(f)
		jf.output({'a':'b'})
		jf.output({"b":"a"})
		jf.close()
		f = open("x.xml","r")
		correct = """<?xml version="1.0"?>
<concordances>
	<item>
		<a>b</a>
	</item>	
	<item>
		<b>a</b>
	</item>	
</concordances>
"""
		a = f.read()
		self.assertTrue(a==correct)
		f.close()

if __name__=='__main__':
	unittest.main()

