import requests
from GoogleScraper.user_agents import random_user_agent

'''This is needed because... TODO
'''

def get_raw_html(url):
	'''Get raw html.

	Sometimes on url doesn't reside html document, but other type, .ppt, .doc,
	.pdf etc. In that case this document is silently returned.

	Args: url
	Returns: content of url request
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
	req = requests.get(url, timeout=10, headers=headers)
	return req.text

# for debugging purposes:
if __name__=="__main__":
	get_raw_html("sdfsfd")
