# -*- coding: utf-8 -*-

'''This module parses Bing SERP. It comes from GoogleScraper.

	https://github.com/NikolaiT/GoogleScraper

, namely from its modules parsing and database. I removed all unnecessary
parts of it, like handling with database and proxy, scraping pictures from
6 seach engines etc., and relieved it from nearly all dependence libraries.
'''

##############################################
# This code was taken from GoogleScraper.
# 
import sys
import re
import lxml.html
from lxml.html.clean import Cleaner
import pprint
import logging
from cssselect import HTMLTranslator
from six.moves.urllib.parse import urlparse


logger = logging.getLogger(__name__)


class SearchEngineResultsPage():

	def has_no_results_for_query(self):
		return self.num_results == 0 or self.effective_query

	def set_values_from_parser(self, parser):
		"""Populate itself from a parser object.

		Args:
			A parser object.
		"""

		self.num_results_for_query = parser.num_results_for_query
		self.num_results = parser.num_results
		self.effective_query = parser.effective_query
		self.no_results = parser.no_results

		for key, value in parser.search_results.items():
			if isinstance(value, list):
				for link in value:
					parsed = urlparse(link['link'])

					# fill with nones to prevent key errors
					[link.update({key: None}) for key in ('snippet', 'title', 'visible_link') if key not in link]

					Link()

	def set_values_from_scraper(self, scraper):
		"""Populate itself from a scraper object.

		A scraper may be any object of type:

			- SelScrape
			- HttpScrape
			- AsyncHttpScrape

		Args:
			A scraper object.
		"""

		self.query = scraper.query
		self.search_engine_name = scraper.search_engine_name
		self.scrape_method = scraper.scrape_method
		self.page_number = scraper.page_number
		self.requested_at = scraper.requested_at
		self.requested_by = scraper.requested_by
		self.status = scraper.status

	def was_correctly_requested(self):
		return self.status == 'successful'

class Link():

	def __str__(self):
		return '<Link at rank {rank} has url: {link}>'.format(**self.__dict__)

	def __repr__(self):
		return self.__str__()



class Parser(object):
	"""Parses SERP pages.

	Each search engine results page (SERP) has a similar layout:
	
	The main search results are usually in a html container element (#main, .results, #leftSide).
	There might be separate columns for other search results (like ads for example). Then each 
	result contains basically a link, a snippet and a description (usually some text on the
	target site). It's really astonishing how similar other search engines are to Google.
	
	Each child class (that can actual parse a concrete search engine results page) needs
	to specify css selectors for the different search types (Like normal search, news search, video search, ...).

	Attributes:
		search_results: The results after parsing.
	"""

	# this selector specified the element that notifies the user whether the search
	# had any results.
	no_results_selector = []

	# if subclasses specify an value for this attribute and the attribute
	# targets an element in the serp page, then there weren't any results
	# for the original query.
	effective_query_selector = []

	# the selector that gets the number of results (guessed) as shown by the search engine.
	num_results_search_selectors = []

	# some search engine show on which page we currently are. If supportd, this selector will get this value.
	page_number_selectors = []

	# The supported search types. For instance, Google supports Video Search, Image Search, News search
	search_types = []

	# Each subclass of Parser may declare an arbitrary amount of attributes that
	# follow a naming convention like this:
	# *_search_selectors
	# where the asterix may be replaced with arbitrary identifier names.
	# Any of these attributes represent css selectors for a specific search type.
	# If you didn't specify the search type in the search_types list, this attribute
	# will not be evaluated and no data will be parsed.

	def __init__(self, config=None, html=None, query=''):
		"""Create new Parser instance and parse all information.

		Args:
			html: The raw html from the search engine search. If not provided, you can parse 
					the data later by calling parse(html) directly.
			searchtype: The search type. By default "normal"
			
		Raises:
			Assertion error if the subclassed
			specific parser cannot handle the the settings.
		"""
		self.config = config
		self.searchtype = "normal"#self.config.get('search_type', 'normal')
		assert self.searchtype in self.search_types, 'search type "{}" is not supported in {}'.format(
			self.searchtype,
			self.__class__.__name__
		)

		self.query = query
		self.html = html
		self.dom = None
		self.search_results = {}
		self.num_results_for_query = ''
		self.num_results = 0
		self.effective_query = ''
		self.page_number = -1
		self.no_results = False

		# to be set by the implementing sub classes
		self.search_engine = ''

		# short alias because we use it so extensively
		self.css_to_xpath = HTMLTranslator().css_to_xpath


		if self.html:
			self.parse()

	def parse(self, html=None):
		"""Public function to start parsing the search engine results.
		
		Args: 
			html: The raw html data to extract the SERP entries from.
		"""
		if html:
			self.html = html

		# lets do the actual parsing
		self._parse()

		# Apply subclass specific behaviour after parsing has happened
		# This is needed because different parsers need to clean/modify
		# the parsed data uniquely.
		self.after_parsing()

	def _parse_lxml(self, cleaner=None):
		try:
			parser = lxml.html.HTMLParser(encoding='utf-8')
			if cleaner:
				self.dom = cleaner.clean_html(self.dom)
			self.dom = lxml.html.document_fromstring(self.html, parser=parser)
			self.dom.resolve_base_href()
		except Exception as e:
			# maybe wrong encoding
			logger.error(e)

	def _parse(self, cleaner=None):
		"""Internal parse the dom according to the provided css selectors.
		
		Raises: InvalidSearchTypeException if no css selectors for the searchtype could be found.
		"""
		self._parse_lxml(cleaner)

		# try to parse the number of results.
		attr_name = self.searchtype + '_search_selectors'
		selector_dict = getattr(self, attr_name, None)

		# get the appropriate css selectors for the num_results for the keyword
		num_results_selector = getattr(self, 'num_results_search_selectors', None)

		self.num_results_for_query = self.first_match(num_results_selector, self.dom)
		if not self.num_results_for_query:
			logger.debug('{}: Cannot parse num_results from serp page with selectors {}'.format(self.__class__.__name__,
																					   num_results_selector))

		# get the current page we are at. Sometimes we search engines don't show this.
		try:
			self.page_number = int(self.first_match(self.page_number_selectors, self.dom))
		except ValueError:
			self.page_number = -1

		# let's see if the search query was shitty (no results for that query)
		self.effective_query = self.first_match(self.effective_query_selector, self.dom)
		if self.effective_query:
			logger.debug('{}: There was no search hit for the search query. Search engine used {} instead.'.format(
				self.__class__.__name__, self.effective_query))

		# the element that notifies the user about no results.
		self.no_results_text = self.first_match(self.no_results_selector, self.dom)

		# get the stuff that is of interest in SERP pages.
		if not selector_dict and not isinstance(selector_dict, dict):
			raise InvalidSearchTypeException('There is no such attribute: {}. No selectors found'.format(attr_name))

		for result_type, selector_class in selector_dict.items():

			self.search_results[result_type] = []

			for selector_specific, selectors in selector_class.items():

				if 'result_container' in selectors and selectors['result_container']:
					css = '{container} {result_container}'.format(**selectors)
				else:
					css = selectors['container']

				results = self.dom.xpath(
					self.css_to_xpath(css)
				)

				to_extract = set(selectors.keys()) - set(['container','result_container'])
				selectors_to_use = dict((key, selectors[key]) for key in to_extract if key in selectors.keys())

				for index, result in enumerate(results):
					# Let's add primitive support for CSS3 pseudo selectors
					# We just need two of them
					# ::text
					# ::attr(attribute)

					# You say we should use xpath expressions instead?
					# Maybe you're right, but they are complicated when it comes to classes,
					# have a look here: http://doc.scrapy.org/en/latest/topics/selectors.html
					serp_result = {}
					# key are for example 'link', 'snippet', 'visible-url', ...
					# selector is the selector to grab these items
					for key, selector in selectors_to_use.items():
						serp_result[key] = self.advanced_css(selector, result)

					serp_result['rank'] = index + 1

					# only add items that have not None links.
					# Avoid duplicates. Detect them by the link.
					# If statement below: Lazy evaluation. The more probable case first.
					if 'link' in serp_result and serp_result['link'] and \
							not [e for e in self.search_results[result_type] if e['link'] == serp_result['link']]:
						self.search_results[result_type].append(serp_result)
						self.num_results += 1

	def advanced_css(self, selector, element):
		"""Evaluate the :text and ::attr(attr-name) additionally.

		Args:
			selector: A css selector.
			element: The element on which to apply the selector.

		Returns:
			The targeted element.

		"""
		value = None

		if selector.endswith('::text'):
			try:
				value = element.xpath(self.css_to_xpath(selector.split('::')[0]))[0].text_content()
			except IndexError:
				pass
		else:
			match = re.search(r'::attr\((?P<attr>.*)\)$', selector)

			if match:
				attr = match.group('attr')
				try:
					value = element.xpath(self.css_to_xpath(selector.split('::')[0]))[0].get(attr)
				except IndexError:
					pass
			else:
				try:
					value = element.xpath(self.css_to_xpath(selector))[0].text_content()
				except IndexError:
					pass

		return value

	def first_match(self, selectors, element):
		"""Get the first match.

		Args:
			selectors: The selectors to test for a match.
			element: The element on which to apply the selectors.

		Returns:
			The very first match or False if all selectors didn't match anything.
		"""
		assert isinstance(selectors, list), 'selectors must be of type list!'

		for selector in selectors:
			if selector:
				try:
					match = self.advanced_css(selector, element=element)
					if match:
						return match
				except IndexError as e:
					pass

		return False

	def after_parsing(self):
		"""Subclass specific behaviour after parsing happened.
		
		Override in subclass to add search engine specific behaviour.
		Commonly used to clean the results.
		"""

	def __str__(self):
		"""Return a nicely formatted overview of the results."""
		return pprint.pformat(self.search_results)

	@property
	def cleaned_html(self):
		# Try to parse the provided HTML string using lxml
		# strip all unnecessary information to save space
		cleaner = Cleaner()
		cleaner.scripts = True
		cleaner.javascript = True
		cleaner.comments = True
		cleaner.style = True
		self.dom = cleaner.clean_html(self.dom)
		assert len(self.dom), 'The html needs to be parsed to get the cleaned html'
		return lxml.html.tostring(self.dom)

	def iter_serp_items(self):
		"""Yields the key and index of any item in the serp results that has a link value"""

		for key, value in self.search_results.items():
			if isinstance(value, list):
				for i, item in enumerate(value):
					if isinstance(item, dict) and item['link']:
						yield (key, i)


class BingParser(Parser):
	"""Parses SERP pages of the Bing search engine."""

	search_engine = 'bing'

	search_types = ['normal', 'image']

	no_results_selector = ['#b_results > .b_ans::text']

	num_results_search_selectors = ['.sb_count']

	effective_query_selector = ['#sp_requery a > strong']

	page_number_selectors = ['.sb_pagS::text']

	normal_search_selectors = {
		'results': {
			'us_ip': {
				'container': '#b_results',
				'result_container': '.b_algo',
				'link': 'h2 > a::attr(href)',
				'snippet': '.b_caption > p::text',
				'title': 'h2::text',
				'visible_link': 'cite::text'
			},
			'de_ip': {
				'container': '#b_results',
				'result_container': '.b_algo',
				'link': 'h2 > a::attr(href)',
				'snippet': '.b_caption > p::text',
				'title': 'h2::text',
				'visible_link': 'cite::text'
			},
			'de_ip_news_items': {
				'container': 'ul.b_vList li',
				'link': ' h5 a::attr(href)',
				'snippet': 'p::text',
				'title': ' h5 a::text',
				'visible_link': 'cite::text'
			},
		},
		'ads_main': {
			'us_ip': {
				'container': '#b_results .b_ad',
				'result_container': '.sb_add',
				'link': 'h2 > a::attr(href)',
				'snippet': '.sb_addesc::text',
				'title': 'h2 > a::text',
				'visible_link': 'cite::text'
			},
			'de_ip': {
				'container': '#b_results .b_ad',
				'result_container': '.sb_add',
				'link': 'h2 > a::attr(href)',
				'snippet': '.b_caption > p::text',
				'title': 'h2 > a::text',
				'visible_link': 'cite::text'
			}
		}
	}

	image_search_selectors = {
		'results': {
			'ch_ip': {
				'container': '#dg_c .imgres',
				'result_container': '.dg_u',
				'link': 'a.dv_i::attr(m)'
			},
		}
	}

	def __init__(self, *args, **kwargs):
		super(BingParser, self).__init__(*args, **kwargs)

	def after_parsing(self):
		"""Clean the urls.

		The image url data is in the m attribute.

		m={ns:"images.1_4",k:"5018",mid:"46CE8A1D71B04B408784F0219B488A5AE91F972E",
		surl:"http://berlin-germany.ca/",imgurl:"http://berlin-germany.ca/images/berlin250.jpg",
		oh:"184",tft:"45",oi:"http://berlin-germany.ca/images/berlin250.jpg"}
		"""
		super(BingParser,self).after_parsing()

		if self.searchtype == 'normal':

			self.no_results = False
			if self.no_results_text:
				self.no_results = self.query in self.no_results_text \
					or 'Do you want results only for' in self.no_results_text

		if self.searchtype == 'image':
			for key, i in self.iter_serp_items():
				for regex in (
						r'imgurl:"(?P<url>.*?)"',
				):
					result = re.search(regex, self.search_results[key][i]['link'])
					if result:
						self.search_results[key][i]['link'] = result.group('url')
						break

# End of GoogleScraper
################################

# this is a way how to use the code from GoogleScraper
def parse(raw_html):
	''':param raw_html -- a html of Bing SERP.

	:returns a list of dict, every dict contains link's useful data from serp.
	It may look like this (pretty printed):

	 {'link': 'http://forvo.com/word/ahoj/',
		'rank': 9,
		'snippet': 'Pronunciation guide: Learn how to pronounce ahoj in Czech, '
							 'Slovak, Polish with native pronunciation. ahoj translation '
							 'and audio pronunciation',
		'title': 'ahoj pronunciation: How to pronounce ahoj in Czech, Slovak ...',
		'visible_link': 'forvo.com/word/ahoj'}
	'''
	parser = BingParser()
	parser.parse(raw_html)
	serp = SearchEngineResultsPage()
	serp.set_values_from_parser(parser)
	parsed_data = parser.search_results['results']

	# there is one strange and useless information, we delete it
	try: del parsed_data["ads_main"]
	except: pass
	return parsed_data


if __name__ == '__main__':
	# note from the author of GoogleScraper:
	"""Originally part of https://github.com/NikolaiT/GoogleScraper.
	
	Only for testing purposes: May be called directly with an search engine 
	search url. For example:
	
	python3 parsing.py 'http://yandex.ru/yandsearch?text=GoogleScraper&lr=178&csg=82%2C4317%2C20%2C20%2C0%2C0%2C0'
	
	Please note: Using this module directly makes little sense, because requesting such urls
	directly without imitating a real browser (which is done in my GoogleScraper module) makes
	the search engines return crippled html, which makes it impossible to parse.
	But for some engines it nevertheless works (for example: yandex, google, ...).
	"""

	# my note
	"""According to my experiment, it works for Bing, but for google doesn't.
	"""
	import requests

	assert len(sys.argv) >= 2, 'Usage: {} url/file'.format(sys.argv[0])
	url = sys.argv[1]

	# my code demonstrating it works
	raw_html = requests.get(url).text
	import pprint
	x = parse(raw_html)
	print(pprint.pformat(x))
