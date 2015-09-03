import requests

'''This is needed because... TODO
'''

def get_raw_html(url):
	'''Get raw html.

	Sometimes on url doesn't reside html document, but other type, .ppt, .doc,
	.pdf etc. In that case this document is silently returned.

	Args: url
	Returns: content of url request
	'''
# TODO: add also user-agent?
# this was it has this:
# User-Agent: python-requests/2.2.1 CPython/3.4.0 Linux/3.13.0-62-generic
	req = requests.get(url, timeout=10)
	return req.text
