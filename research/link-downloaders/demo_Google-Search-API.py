from google import google
num_page = 1
search_results = google.search("MIT", num_page)

for i in search_results:
	print i
#		,i.name # The title of the link
#		,i.link # The external link (NOT implemented yet)
#		,i.google_link # The google link
#		,i.description # The description of the link
#		,i.thumb # The link to a thumbnail of the website (NOT
##,implemented yet)
#		,i.cached # A link to the cached version of the page
##,(NOT implemented yet)
#		,i.page # What page this result was on (When
##,searching more than one page)
#		,i.index # What index on this page it was on
		#)
	print
	print i.google_link
	print i.description
	for j in range(3):
		print "--------------------------------------------------------------"
