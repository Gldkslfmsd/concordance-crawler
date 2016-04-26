import requests
from ConcordanceCrawler.core.user_agents import random_user_agent
import stopit

'''A funcion that downloads content from url.
'''

class UrlRequestException(Exception):
	'''Problem during processing of urlrequest'''


def request_get(*args,**kwargs):
	try:
		y = requests.get(*args,**kwargs)
		return y
	# without this it would write stack trace when the application is aborted
	except KeyboardInterrupt:
		pass
	except TypeError:
		print("type error in request_get")

def get_raw_html(url):

	headers = { 'User-Agent': random_user_agent() }

	# abortion of processing after 60 seconds
	with stopit.ThreadingTimeout(60) as timeout:
		req = request_get(url, # function arguments
			{'timeout':10,'headers':headers} # keyword arguments
		)
	
	if timeout.state != stopit.ThreadingTimeout.EXECUTED:
		raise UrlRequestException()

	return req.text, req.headers

# for debugging purposes:
if __name__=="__main__":

	# an url which generates socket.timeout exception
#	print(get_raw_html("http://www.njrtvu.com/kgy/review.asp?id=270"))
	#print(get_raw_html("http://atrey.karlin.mff.cuni.cz:12345"))
	try:
		print("waukeshacounty")
		print(get_raw_html("https://www.waukeshacounty.gov/Product_Disp/"))
	except:
		pass
	print("cd.cz")
	print(get_raw_html("http://cd.cz/"))
