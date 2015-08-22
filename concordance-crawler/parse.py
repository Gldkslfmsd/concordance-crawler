#!/usr/bin/python

from GoogleScraper.parsing import *
import requests

import bazwords

def parseBing(rawhtml):
	"""Gets and parses Bing SERP.

	Returns:
		data from page, parsed and prettyprinted  by GoogleScraper parser
		(it's string, but looks like json)
	"""
	#rawhtml = requests.get(url).text
	#f = open("raw_"+bazwords.RandomShortWords().get_bazword()+".html","w")
	#f.write(rawhtml)
	#f.close()
	
	parser = BingParser(query="")
	parser .parse(rawhtml)

	serp = SearchEngineResultsPage()
	serp.query = ""
	serp.set_values_from_parser(parser)
	serp.search_engine_name = "bing"

	parsed_data = str(parser)
	return parsed_data
