from json import dumps
from dict2xml import dict2xml

'''Output formatter classes.

This classes gradually write list of concordances to output file-like
object. It's necessary to write the concordances gradually and instantly after
they are crawled, because user can see that the crawler works and he can
control progress of a program. The second result is that otherwise they
should be stored in memory, but it shouldn't be so big.
'''

class OutputFormatter():
	'''Common ancestor of formatters with defined format. This is de facto
	abstract class.'''

	def __init__(self, output_stream):
		'''
		Args:
			output_stream -- a file-like object
		'''
		self.output_stream = output_stream

	def close(self):
		# every formatter must close the file in the end
		self.output_stream.close()

	# this is static method
	def create_formatter(format,output_stream):
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
			return JsonFormatter(output_stream)
		elif format=='xml':
			return XmlFormatter(output_stream)
		else:
			raise ValueError("format must be \'json\' or \'xml\'")

class JsonFormatter(OutputFormatter):
	'''Writes pretty-printed concordances in json.
	'''
	def __init__(self,output_stream):
		super().__init__(output_stream)
		# writes [ to output as a begining symbol of list of concordances...
		self.output_stream.write("[")
		self.first = True

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
		result = comma + dumps([concordance],indent=' '*4)[2:-2]
		self.output_stream.write(result)

	def close(self):
		# ...and terminating ] of list
		self.output_stream.write("\n]\n")
		super().close()
	
class XmlFormatter(OutputFormatter):
	'''Writes pretty-printed concordances in xml.
	'''
	def __init__(self,output_stream):
		super().__init__(output_stream)
		self.output_stream.write("<root>\n")

	def output(self,concordance):
		'''writes a concordance in xml format to output_stream
		
		Args:
			concordance: concordance as a dict
		'''
		result = dict2xml({'item':concordance},indent=" "*4,wrap="") + "\n"
		self.output_stream.write(result)

	def close(self):
		self.output_stream.write("</root>\n")
		super().close()
