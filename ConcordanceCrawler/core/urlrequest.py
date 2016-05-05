import requests
from ConcordanceCrawler.core.user_agents import random_user_agent
import stopit

'''A funcion that downloads content from url.
'''

class UrlRequestException(Exception):
	'''Problem during processing of urlrequest'''


TIMEOUTLIMIT = 60
SIZELIMIT = 20 * 1024 ** 2  # 20 MB

def get_raw_html(url):

	headers = { 'User-Agent': random_user_agent() }

	# abortion of processing after 60 seconds
	with stopit.ThreadingTimeout(TIMEOUTLIMIT) as timeout:
		resp = requests.get(url,timeout=10,headers=headers)
	
	if timeout.state != stopit.ThreadingTimeout.EXECUTED:
		raise UrlRequestException()

	# headers is CaseInsensitiveDict, because http header fieldnames are case insensitive
	if ('Content-Type' in headers and not 'text' in headers['Content-Type']):
		raise ValueError("document is not text")

	def is_int(value):
		try:
			int(value)
		except ValueError:
			return False
		return True

	if ('content-length' in resp.headers and is_int(resp.headers['content-length']) and int(resp.headers['content-length']) > SIZELIMIT) or \
		len(resp.content) > SIZELIMIT:  # document is greater than 20 MB
		raise ValueError("document is too long")

	return resp.text, resp.headers






# for debugging purposes:
if __name__=="__main__":

	#print(get_raw_html("http://httpbin.org/absolute-redirect/30"))
	a = "http://ambit.tiddlyspace.com/"
	#print(get_raw_html(a))
	
	print(get_raw_html("http://cve.mitre.org/data/downloads/allitems.html"))
