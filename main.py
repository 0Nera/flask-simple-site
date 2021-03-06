from flask import Flask, url_for, render_template, request, make_response, redirect, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image, ImageDraw
from datetime import datetime



app = Flask(
	__name__, 
	template_folder = "templates", 
	static_folder = "static"
)



limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute"]
)


app.config['SECRET_KEY'] = 'a really really really really long secret key'
img_counter = 0
app.secret_key = "super secret key"
app.debug = True



def has_no_empty_params(rule):
	defaults = rule.defaults if rule.defaults is not None else ()
	arguments = rule.arguments if rule.arguments is not None else ()
	return len(defaults) >= len(arguments)


@app.route('/login/', methods=['post', 'get'])
def login():
    return render_template('login.html')


@limiter.limit("10/minute")
@app.route('/gen-img')
def gen_img():
	now = datetime.now()
	global img_counter
	img_counter += 1
	text = "Hello, World!\nGenerated: " + str(img_counter) + "\nServer time: " + str(now) + "\nThis site created on Flask framework\n\nSource code: https://github.com/0Nera\n©2021 Aren Elchinyan"
	color = (0, 0, 120)
	img = Image.new('RGB', (256, 128), color)
	imgDrawer = ImageDraw.Draw(img)
	imgDrawer.text((10, 10), text)
	img.save("static/temp/temp.png")
	return make_response(
		render_template("gen-img.html"), 
		200
		) 


@app.route('/')
def index():
	links = []
	for rule in app.url_map.iter_rules():
		if "GET" in rule.methods and has_no_empty_params(rule):
			url = url_for(rule.endpoint, **(rule.defaults or {}))
			links.append((url, rule.endpoint))
	return make_response(
		render_template("index.html", 
			links=reversed(links),
			ip=request.remote_addr,
			browser=request.user_agent
			), 
		200
		)


@app.route('/admin')
def admin():
    return '200'


@app.route('/session-test')
def session_test():
	if 'visits' in session:
		session['visits'] = session.get('visits') + 1  # чтение и обновление данных сессии
	else:
		session['visits'] = 1  # настройка данных сессии
	return make_response(
		render_template("session-test.html", 
			visits=session.get('visits')
			), 
		200
		)


@app.route('/session-pop')
def session_pop():
	session.pop('visits', None)
	return redirect(
		url_for("session_test"), 
		code=200
		)


@app.route('/about')
def about():
	return make_response(
		render_template("about.html"
			),
		200
		)


@app.route("/redirect/<url>")
def redirect_to(url):
	return make_response(
		redirect(url), 
		200
		)



if __name__ == "__main__":
	app.run()