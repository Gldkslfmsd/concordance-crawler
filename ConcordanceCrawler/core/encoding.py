import re

def norm_encoding(document, headers, allowed="utf-8"):
	'''This method should return document in normalized encoding or None. If None,
	document will be skipped from extraction.
	
	In fact this only returns the same document or None. If the document is html and
	there is metatag specifying `allowed` encoding, or the encoding is given in http response headers,
	and these two values are not unequal, then the `document` is returned, None otherwise.
	'''
	# missing Content-Type header
	if not 'Content-Type' in headers:
		return None
	
	h = headers['Content-Type']
	# charset in header is present and is different from utf-8
	charset = "harset=" in h
	if charset and not allowed in h and not allowed.upper() in h:
		return None

	# charset in header is missing or is utf-8
	
	m = re.search(r"charset=\S*", document)
	if m:	 # meta tag containing charset is presented in html
		x = m.string[m.start():m.end()]
		x = re.sub(r"['\"]","",x)
		x = re.sub(r"charset=","",x)
		x = re.sub(r"[</>;\"].*",r"",x)
		if x.lower()==allowed:  # charset in meta tag is utf-8
			return document
		return None  # charset in meta tag is not utf-8

	
	if charset:  # charset was present in header, but not in meta tag
		return document
	return None  # charset unspecified



if __name__ == "__main__":
	meta_utf = 'sdfas <meta charset="utf-8"'
	meta_UTF = 'sdfas <meta charset="UTF-8"'

	header_utf = 	{"Content-Type": "text/html; charset=UTF-8;"}
	header_ct_nothing = {"Content-Type": "text/html;"}
	header_iso = {"Content-Type": "text/html; charset=iso-8859-1;"}

	true = [
		(meta_utf, header_utf),
		(meta_UTF, header_utf),
		(meta_utf, header_ct_nothing),
		("sfdasdfsa charset=\"utf-8\"",header_utf),
		("sfdasdfsa charset=\"utf-8;sdfs \"",header_utf),
		("sfdasdfsa charset=\"utf-8;sdfs \"",header_ct_nothing),
		("sfdasdfsa charset=utf-8 ;sdfs \"",header_utf),
		("sfdasdfsa charset=utf-8 ;sdfs \"",header_ct_nothing),
		("sfdasdfsa charset='utf-8' ;sdfs \"",header_utf),
		("sfdasdfsa charset='utf-8' ;sdfs \"",header_ct_nothing),

		]

	false = [
		(meta_utf, {}),
		("sfdasdfsa fsdfasfdsa fdsfdasfdsa charset=sdfafdsafasfasf",header_utf),
		("sfdasdfsacharset=utf-16",header_utf),
		("sfdasdfsa charset=\"iso-8859-1\"",header_utf),
		("sfdasdfsa ",header_iso),
		("sfdasdfsa ",header_ct_nothing),
		(meta_utf, header_iso),




		]


	for a,b in true:
		x = norm_encoding(a, headers=b)
		print("|",x+"x","W")

	for a,b in false:
		x = norm_encoding(a, headers=b)
		print("nic:",x)




