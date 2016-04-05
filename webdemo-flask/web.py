from flask import Flask, send_from_directory, url_for, redirect
app = Flask(__name__)

main_page = """<html>
<head>
	<meta http-equiv='content-type' content='text/html; charset=utf-8'/>
	<title>ConcordanceCrawler</title>

	<link rel="shortcut icon" href="static/favicon.png">
	<link rel='stylesheet' type='text/css' href='static/styles.css'/>
	<script type='text/javascript'	src='static/jquery-1.7.1.min.js'></script>
	<script type='text/javascript' src='static/applets.js'></script>
</head>

<body>
něco
</body>
</html>
"""

@app.route("/")
def root():
	return main_page

@app.route("/images/<path:image>")
def images(image):
	return 

@app.route("/javascript/<path:name>")
def send_js(name):
	return app.send_static_file("javascript/"+name)



if __name__ == "__main__":
	app.debug=True
	app.run()
