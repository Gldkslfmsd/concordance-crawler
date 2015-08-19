#!/usr/bin/python

from GoogleScraper.parsing import *
import requests

def parseBing(url):
	"""Gets and parses Bing SERP.

	Returns:
		data from page, parsed and prettyprinted  by GoogleScraper parser
		(it's string, but looks like json)
	"""
	rawhtml = requests.get(url).text
	g = BingParser(query="")
	g.parse(rawhtml)

	serp = SearchEngineResultsPage()
	serp.query = ""
	serp.set_values_from_parser(g)
	serp.search_engine_name = "bing"

	return str(g)
