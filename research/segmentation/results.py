'''prints the results of demos pretty and uniformly'''

import pprint
def print_results(sentences):
	for s in sentences:
		s = pprint.pformat(s)
		print(s)
		print()
