import re
import segtok.segmenter as segmenter

def sentence_segmentation(text):
	return list(segmenter.split_multi(text))


