import re
from ConcordanceCrawler.core.limited_buffer import LimitedBuffer
from ConcordanceCrawler.app.output_formatter import create_formatter


def is_row(tag, line):
	return re.match('^\s*"'+tag+'"',line) or \
		line.startswith('\t\t<'+tag+'>')

def extract_value(tag, line, format):
	if format=='xml':
		m = re.search(r'>([^<]*)<', line)
		value = m.groups()[0]
	elif format=='json':
		start = len('        "'+tag+'": "')
		end = len('",\n')
		value = line[start:-end]
	return value
	

def load_from_corpus(filename, format):
	assert format in ("xml", "json"), "unknown format"
	maxid = 0
	links = LimitedBuffer()
	concordances = LimitedBuffer()
	with open(filename, "r") as f:
		for line in f:
			if is_row('id', line):
				m = re.search(r"\d+",line)
				id = int(line[m.start():m.end()])
				maxid = max(id, maxid)
			elif is_row('concordance',line):
				concordance = extract_value('concordance', line, format)
				concordances.insert(concordance)
			elif is_row('url', line):
				url = extract_value('url', line, format)
				links.insert(url)

	if maxid==0:
		mode = "w"
	else:
		mode = "a"

	outstream = open(filename, mode)
	of = create_formatter(
		format=format,
		output_stream=outstream,
		extending= maxid!=0,
		)
	return {
		'links':links,
		'concordances':concordances,
		'maxid':maxid,
		'output': outstream,
		'formatter': of,
	}
				

if __name__ == "__main__":
	print(load_from_corpus("word.json","json"))
	print(load_from_corpus("word.xml", "xml"))
