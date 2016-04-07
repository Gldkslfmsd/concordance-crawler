from flask import Flask, send_from_directory, url_for, redirect, request
app = Flask(__name__)

from model import *
from time import ctime

@app.route("/", methods=["GET", "POST"])
def root():
	if request.method=="GET":
		return app.send_static_file("main.html")

@app.route("/newjob", methods=["POST"])
def newjob():
	if request.form['target'] == '':
		return 'target word cannot be empty'
	res = create_new_job(request.form)
	return str(res)

resp = """[OK]
20,0,10,ctime,DESC
sdfsa,2016-04-05 21:25:23,410 Error occured during document processing in treex.
martin_nda_cleansed,2015-12-09 15:52:27,410 Error occured during document processing in treex.
martin_NDA,2015-12-09 15:42:50,720 Document exported successfully.
14,2015-10-19 14:19:02,720 Document exported successfully.
propredvedeni2,2015-09-24 07:48:29,720 Document exported successfully.
propredvedeni1,2015-09-23 23:03:37,720 Document exported successfully.
socialnipodpora1,2015-09-23 22:36:00,720 Document exported successfully.
zakonucetnictvi2,2015-09-23 22:17:44,720 Document exported successfully.
test12,2015-09-23 21:34:34,720 Document exported successfully.
"""

@app.route("/listjobs/start=<int:start>/limit=<int:limit>/order_by=<path:orderby>/order_dir=<path:orderdir>")
def listjobs(start, limit, orderby, orderdir):
	response = "[OK]\n"
	jobids = browse_jobs()
	response += ",".join(map(str,(str(len(jobids)), start, limit, orderby, orderdir)))+"\n"
	jobdata = []
	for j in jobids:
		jobdata.append([
			get_target(j),
			get_time(j),
			get_status(j),
			])
	
	reverse = True if orderdir == "DESC" else False	
	
	if orderby == 'ctime':
		key=lambda jd: jd[1]
	elif orderby == 'id':
		key=lambda jd: jd[0]
	else:
		key=lambda jd: jd[2]
	jobdata = sorted(jobdata, key=key, reverse=reverse)[start:start+limit]

	for data in jobdata:
		data[1] = ctime(data[1]).strip()
		response += ",".join(data)+"\n"
	return response
	

if __name__ == "__main__":
	app.debug=True
	app.run()
