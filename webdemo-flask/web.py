from flask import Flask, send_from_directory, url_for, redirect, request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def root():
	if request.method=="GET":
		return app.send_static_file("main.html")

@app.route("/newjob", methods=["POST"])
def newjob():
	print(request.form)
	if request.form['target'] == '':
		return 'target word cannot be empty'
	return 'OK'+str(request.form)
	

if __name__ == "__main__":
	app.debug=True
	app.run()
