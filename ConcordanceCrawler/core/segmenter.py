import re
def sentence_segmentation(text):
	# NOTE: ... (three dots) get lost, but that would be too complicated

	# cut text to list: [ sentence, delimiter, sentence, delimiter, ... ]
	# e.g. [ "Hello", "!", " How are you", "?", "I'm fine", "." ]
	chunks = re.split("([\n\.\?\!])",text)
	
	# join sentence and its terminal mark
	# -> [ "Hello!", " How are you?", "I'm fine." ]
	sentences = [ x+y for x,y in zip(chunks[::2],chunks[1::2]) ]
	
	return sentences
