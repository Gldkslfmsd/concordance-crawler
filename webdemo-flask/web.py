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

<div id='header'>
	<div id='header_content'>
		<h1>ConcordanceCrawler</h1>
<!--		<img src='static/logo.png' class='header-logo'>
-->
	</div>
</div>


<div id='content'>
	<div id='left-column'>
		<!-- Menu -->

		<div class='box'>
			<h2>Menu</h2>
			<ul>
				<li><a href='javascript:run_text("welcome");'>Home</a>
				<li><a href='javascript:run_text("about");'>About</a>
				<li><a href='javascript:run_submit()'>Submit new job</a>
				<li><a href='javascript:run_list();'>Browse submitted jobs</a>
				<li><a href='javascript:run_list();'>Download corpora</a>
				<li><a href='javascript:run_text("contact");'>Contact</a>
			</ul>
		</div>


		<div class='box' id='applet_server_status'>
			<h2>Server status</h2>
			<div class='loading'></div>
			<div class='data'></div>
		</div>
	</div>

	<div id='main-column'></div>
	<div style='clear: both'></div>
</div>

<div id='footer'>
	<p>2016 Dominik Macháček</p>
</div>

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
