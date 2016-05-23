from flask import Flask, send_from_directory, url_for, redirect, request
app = Flask(__name__)

from model import *
from time import ctime, time
import random
import os.path

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
			j,
			get_percent_str(j)
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
		data[1] = get_ctime(data[3])
		response += ",".join(data)+"\n"
	return response


resp = """[OK]
400 Language processing started.
Submition time: 2016-04-08 11:09:14
Extraction strategy: intlib_en
"""

@app.route("/jobdetail/<path:jobid>")
def jobdetail(jobid):
	resp = [ "[0K]",  # response status 0
		get_status(jobid),  # status 1
		get_ctime(jobid),  # submition ctime 2
		get_percent_str(jobid),  # percent 3
		get_target(jobid),  # target 4
		] + get_crawling_status(jobid)  # raw crawling status 5 -- 8
	resp += [  # job parameters
		get_target(jobid), # 9
		get_pos(jobid), # 10
		get_number_of_concordances(jobid),
		get_max_per_page(jobid),
		get_english_filter(jobid),
		get_bazgen(jobid),
		get_encoding(jobid),
		] + [
		get_concordances_crawled(jobid),  # 15
		]
	return "\n".join(map(str,resp))

@app.route("/deletejob/<path:jobid>")
def deletejob(jobid):
	return "["+delete_job(jobid)+"]"
	

@app.route("/concordances/<path:jobid>")
def concordances(jobid,start=0,limit=100):
	corpus = get_corpus(jobid, start, limit)
	return "[OK]\n"+"".join(corpus)


last_call = 0  # time where jobmanager was last seen living
@app.route("/serverstatus")
def serverstatus():
	global last_call
	if os.path.isfile("jobmanager_livestamp"):
		print("žije", last_call)
		os.remove("jobmanager_livestamp")
		last_call = time()
	else:
		print("nežije", last_call)
	tnow = time()
	if tnow - last_call > 10:
		return "[OK]\nServer is OFF"
	return "[OK]\nServer is ON"

if __name__ == "__main__":
	#app.debug=True
	app.run("0.0.0.0",port=81, threaded=True)
