#!/usr/bin/env python3

'''Experiment:
'''

# this comes from concordance crawler, but it may change, so I copy this
# instead of importing:

def get_keyword_url(keyword):
	replacedspaces = keyword.replace(" ","+")
	url = "https://www.google.cz/search?q={keyword}".format(
		keyword = replacedspaces
	)
	return url

"""Bazwords generators:"""

import random
class RandomShortWords():
	"""Generates bazwords that look like 4 random letters"""
	# this is list of all letters
	letters = [ chr(a) for a in range(ord('a'),ord('z')+1) ]
	def __init__(self,seed = None):
		if seed:
			random.seed(seed)

	def get_bazword(self):
		baz = ""
		for i in range(4):
			baz += random.choice(self.letters)
		return baz
	
# (end of concordance crawler)

import datetime
import time
import multiprocessing

def events_per_minute(number,seconds=60,event=lambda _:0):
	'''
	Regularly starts event.

	Args:
		number: number of events in given time
		seconds: the length of experiment
		event: a function which is called asynchronously
	'''
	count = 0
	print("Beginning...")
	print(count, str(datetime.datetime.now()))

	span = seconds/number
	pool = multiprocessing.Pool(50)
	while count < number:
		now = time.time()
		future = now + span
		# we wait until our time comes
		# (active waiting is inefficient, but easy)
		while time.time() < future:
			pass
#		print(count, str(datetime.datetime.now()))
		count += 1
		# start event asynchronously in a pool
		pool.apply_async(event,[count])
	print(str(datetime.datetime.now()),"joining processes...")
	# we wait until the processes finish
	pool.close()
	pool.join()
	print(str(datetime.datetime.now()),"finished")

rsw = RandomShortWords(0)

import requests

def one_scrape(id):
	'''scrapes one keyword, saves result page to file and tests success
	
	Args:
		id -- number of attempt
	'''
	# keyword will be a random bazword and a word "employ", you can change it
	url = get_keyword_url(rsw.get_bazword() + " employ")
	rawhtml = requests.get(url).text
	f = open("raw_google_"+str(id)+".html","w")
	f.write(rawhtml)
	f.close()
	if is_blocked(rawhtml):
	# here you can see an id of query and it's result, blocked, if bing replied
	# a page with captcha or ok, if replied a page with results (probably)
		print("\t",id,"blocked")
	else:
		print("\t",id,"ok")

def is_blocked(rawhtml):
	'''this is an easy and quick control of blocked file with captcha

	Returns:
		True if the query was blocked
		False otherwise
	'''
	# sometimes you get 115 bytes file with a strange code (e.g. if you try 30000
	# requests per minute)
	if len(rawhtml)<120:
		return True 

	# I can see this in Czech Republic, in other countries it may differ!
	return 'Omluvte přerušení' in rawhtml



# with this configuration your experiment will last 60 seconds and you try
# 37 requests (which is maximum)
sec = 10
events_per_minute(3*sec,seconds=sec,event=one_scrape)
