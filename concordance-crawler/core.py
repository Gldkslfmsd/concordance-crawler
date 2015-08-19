#!/usr/bin/env python3

# This will be a main file of Concordance Crawler. 
# This version uses whole GoogleScraper.

from GoogleScraper import scrape_with_config, GoogleSearchError

from GoogleScraper import output_converter

from os import remove


def crawl(bazwords, word):
	'''Starts scraping with a set of keywords. A keyword is a particular
	bazword + word
	
	Args:
		bazwords -- list of bazwords
		word -- a concordance

	Returns:
		nothing, you can find the input in a file concordances.json
		@TODO
	'''
	# delete output file from previous run
	open('concordances.json','w').close()
	concordances = open('concordances.json','a')
	for i in bazwords:
		crawlonekeyword(i + " " + word)
		f = open('tmp.json','r')
		crawled = f.read()
		concordances.write(crawled)
		f.close()
	concordances.close()
	remove('tmp.json')

config = {
		'SCRAPING': {
				'use_own_ip': 'True',
				'search_engines': 'bing',
				'num_pages_for_keyword': 100,
				'check_proxies': 'False',
				'num_workers': 10,
				'num_results_per_page': 10,
				'scrape_method': 'http-async',
		},
		'GLOBAL': {
				'do_caching': 'False',
#				'proxy_file': 'proxy'
		},
		'OUTPUT': {
				'database_name': 'concordances',
				'output_filename': 'tmp.json'
		}
}

def crawlonekeyword(keyword):
	'''Scrapes one keyword.

	Args:
		keyword
	Returns:
		The same as GoogleScraper.scrape_with_config, it's a "scaper search
		object"
	'''
	config['SCRAPING']['keyword'] = keyword
	try:
		search = scrape_with_config(config)
	except GoogleSearchError as e:
		print(e)
	return search
	

crawl(["sdfs","ěščěšč","hšřs"],"rain")
