import six
if six.PY2:
	from simplejson import dumps
	def correct_encode(string):
		return string.encode('utf-8')
else:
	from json import dumps
	def correct_encode(a):
		return a

'''Output formatter classes.

This classes gradually write list of concordances to output file-like
object. It's necessary to write the concordances gradually and instantly after
they are crawled, because user can see that the crawler works and he can
control progress of a program. The second result is that otherwise they
should be stored in memory, but it shouldn't be so big.
'''

class OutputFormatter(object):
	'''Common ancestor of formatters with defined format. This is de facto
	abstract class.'''

	def __init__(self, output_stream):
		'''
		Args:
			output_stream -- a file-like object
		'''
		self.output_stream = output_stream

	def flush(self):
		self.output_stream.flush()

	def close(self):
		# every formatter must close the file in the end
		self.output_stream.close()

def create_formatter(format,output_stream,extending):
	'''creates output formatter for given format

	Args:
		format -- string "xml" or "json"
		output_stream -- output file for formatter

	Returns:
		newly created formatter

	Raises:
		ValueError, if format is not "json" or "xml"
	'''
	if format=='json':
		return JsonFormatter(output_stream,extending)
	elif format=='xml':
		return XmlFormatter(output_stream,extending)
	else:
		raise ValueError("format must be \'json\' or \'xml\'")

class JsonFormatter(OutputFormatter):
	'''Writes pretty-printed concordances in json.
	'''
	def __init__(self,output_stream,extending=False):
		super(JsonFormatter, self).__init__(output_stream)
		# writes [ to output as a begining symbol of list of concordances...
		if not extending:
			self.output_stream.write("[")
			self.first = True
		else:
			self.first = False

	def output(self,concordance):
		'''writes a concordance in json format to output_stream
		
		Args:
			concordance: concordance as a dict
		'''
		if self.first:
			self.first = False
			comma = "\n"
		else:
			# ...comma is just before not-first item in list...
			comma = ",\n"

		# Awful trick how to let it pretty printed:
		# Let's pretend I want to print [concordance] (read: list containing
		# a concordance) instead of concordance. This makes correct indentation.
		# Then I cut leading and terminating "[\n" and "\n]". This trick is
		# needful because I'm printing just one concordance per one call of this
		# function, but together I want a whole list. There isn't any option to
		# make an extra indent for every row.
		result = comma + dumps([concordance],indent=' '*4,ensure_ascii=False)[2:-2]
		self.output_stream.write(correct_encode(result))
		self.flush()

	def close(self):
		# ...and terminating ] of list
		self.output_stream.write("\n]\n")
		super(JsonFormatter, self).close()
	
class XmlFormatter(OutputFormatter):
	'''Writes pretty-printed concordances in xml.
	'''
	def __init__(self,output_stream,extending=False):
		super(XmlFormatter, self).__init__(output_stream)
		if not extending:
			self.output_stream.write('<?xml version="1.0"?>\n')
			self.output_stream.write("<concordances>\n")

	def escape(self,string):
		rep = [
			("&", "&amp;"),
			("<", "&lt;"),
			(">", "&gt;"),
			('"', '&lt;'),
			("'", "&apos;"),
		]
		for what, forwhat in rep:
			string = string.replace(what, forwhat)
		return string
		
	def tag(self,key,value,endsep=""):
		ekey = self.escape(key)
		evalue = self.escape(str(value))
		eendsep = self.escape(endsep)
		return "<"+ekey+">"+evalue+eendsep+"</"+ekey+">"


	def output(self,concordance):
		'''writes a concordance in xml format to output_stream
		
		Args:
			concordance: concordance as a dict
		'''
		xml = "\t<item>"+ "\n\t\t"+"\n\t\t".join(self.tag(k,v) for k,v in concordance.items())+"\n\t"+ "</item>\t\n"
		self.output_stream.write(xml)
		self.flush()

	def close(self):
		self.output_stream.write("</concordances>\n")
		super(XmlFormatter, self).close()

if __name__ == "__main__":
	from sys import stdout
	form = create_formatter("xml", stdout)
	form.output({"a":5,"csdfsdf":None})
	form.output({"a":5})

#	form.close()

	form = create_formatter("xml", stdout)
	form.output({"a":5,"cs><neco><sdf":None})
	form.output({"a":5})

	form.close()


