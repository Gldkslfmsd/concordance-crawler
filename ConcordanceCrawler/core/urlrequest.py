import six
if six.PY3:
	import sys
	if sys.version_info.minor>=4:
		from multiprocessing.context import TimeoutError as multiprocessing_TimeoutError
	else:
		from multiprocessing import TimeoutError as multiprocessing_TimeoutError
elif six.PY2:
	from multiprocessing import TimeoutError as multiprocessing_TimeoutError

import requests
from ConcordanceCrawler.core.user_agents import random_user_agent
import multiprocessing

'''A funcion that downloads content from url.
'''

import time

def request_get(*args,**kwargs):
	try:
		y = requests.get(*args,**kwargs)
		return y
	# without this it would write stack trace when the application is aborted
	except KeyboardInterrupt:
		pass
	except TypeError:
		print("type error in request_get")


# we use just one pool for all calls, because it spares time, memory and
# processes
pool = multiprocessing.Pool(1)
def get_raw_html(url):
	'''Get raw html.

	Sometimes on url doesn't reside html document, but other type, .ppt, .doc,
	.pdf etc. In that case this document is silently returned.

	Args: url
	Returns: content of url request

	Raises:
		multiprocessing.context.TimeoutError -- if a process lasts too long
		other errors like requests.RequestException or its descendants
	'''

# User-Agent is a field in http header, some servers vary documents
# according this header. Machines or automatic crawlers can get different
# document (e.g. a message that automatic traffic is blocked) than living humans
# with webbrowser. Default User-Agent of requests library looks like
# this:
# User-Agent: python-requests/2.2.1 CPython/3.4.0 Linux/3.13.0-62-generic
# Server would immediately know that this is a crawler, so we change it to
# value of currently usual browsers.
# See this link for more details:
# https://github.com/NikolaiT/GoogleScraper/blob/master/GoogleScraper/user_agents.py
	headers = { 'User-Agent': random_user_agent() }

# We must also add timeout, because otherwise whole crawler could be stuck
# for hours if some server wouldn't reply. This timeout is 10 seconds.

# Sometimes it get stuck on requests.get command without known reason, so
# we run this command in side process and measure its time, if it
# lasts more than 5 minutes we kill it.

	try:
		# run it in a pool
		app_res = pool.apply_async(
			request_get, # a function
			(url,), # function arguments
			{'timeout':10,'headers':headers} # keyword arguments
			)
		# waits maximally 5 minutes for result
		req = app_res.get(15)
	except multiprocessing_TimeoutError:
		raise requests.exceptions.Timeout
	except TypeError:
		print("typerror")

	return req.text, req.headers

# for debugging purposes:
if __name__=="__main__":
#	print(get_raw_html("http://cd.cz/"))

	# an url which generates socket.timeout exception
#	print(get_raw_html("http://www.njrtvu.com/kgy/review.asp?id=270"))
	#print(get_raw_html("http://atrey.karlin.mff.cuni.cz:12345"))
	print(get_raw_html("https://www.waukeshacounty.gov/Product_Disp/"))
