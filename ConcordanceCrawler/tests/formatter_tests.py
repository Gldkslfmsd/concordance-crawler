import unittest
from ConcordanceCrawler.app.output_formatter import JsonFormatter

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

if __name__=='__main__':
	unittest.main()
