from flask import Flask, send_from_directory, url_for, redirect, request
app = Flask(__name__)

from model import *

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
	

if __name__ == "__main__":
	app.debug=True
	app.run()
