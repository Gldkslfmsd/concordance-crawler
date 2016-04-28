import requests
from ConcordanceCrawler.core.user_agents import random_user_agent
import stopit

'''A funcion that downloads content from url.
'''

class UrlRequestException(Exception):
	'''Problem during processing of urlrequest'''


TIMEOUTLIMIT = 60

def get_raw_html(url):

	headers = { 'User-Agent': random_user_agent() }

	# abortion of processing after 60 seconds
	with stopit.ThreadingTimeout(TIMEOUTLIMIT) as timeout:
		req = requests.get(url,timeout=10,headers=headers)
	
	if timeout.state != stopit.ThreadingTimeout.EXECUTED:
		raise UrlRequestException()

	return req.text, req.headers






# for debugging purposes:
if __name__=="__main__":

	#print(get_raw_html("http://httpbin.org/absolute-redirect/30"))
	a = "http://ambit.tiddlyspace.com/"
	print(get_raw_html(a))
