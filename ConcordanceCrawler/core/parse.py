#!/usr/bin/python

from GoogleScraper.parsing import *
import requests

def parseBing(rawhtml):
	"""Gets and parses Bing SERP.

	Returns:
		List of dicts, every dict is one link and contains this keys: 
		link, rank, snippet, title, visible_link
	"""

	parser = BingParser()
	parser.parse(rawhtml)

	serp = SearchEngineResultsPage()
	serp.set_values_from_parser(parser)

	# this extracts just the list of dicts
	parsed_data = parser.search_results['results']

	# there is one strange and useless information
	try: del parsed_data["ads_main"]
	except: pass

	return parsed_data
