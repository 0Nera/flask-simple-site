from flask import Flask, url_for, render_template, request, make_response, redirect, session
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
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
db = SQLAlchemy(app)
img_counter = 0
login_manager = LoginManager(app)
login_manager.init_app(app)
app.secret_key = "super secret key"
app.debug = True



def has_no_empty_params(rule):
	defaults = rule.defaults if rule.defaults is not None else ()
	arguments = rule.arguments if rule.arguments is not None else ()
	return len(defaults) >= len(arguments)


@app.route('/login/', methods=['post', 'get'])
def login():
    return render_template('login.html')


@limiter.limit("12/minute")
@login_manager.user_loader
@app.route('/gen-img')
def gen_img():
	now = datetime.now()
	global img_counter
	img_counter += 1
	text = "Hello, World!\nGenerated: " + str(img_counter) + "\nServer time: " + str(now) + "\nThis site created on Flask framework\n\n©2021 Aren Elchinyan\nSource code: https://github.com/0Nera"
	color = (0, 0, 120)
	img = Image.new('RGB', (256, 128), color)
	imgDrawer = ImageDraw.Draw(img)
	imgDrawer.text((10, 10), text)
	img.save("static/img/temp.png")
	return make_response(
		render_template("gen-img.html"), 
		200
		) 


@limiter.limit("1/second")
@login_manager.user_loader
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
@login_required
def admin():
    return '200'


@login_manager.user_loader
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


@login_manager.user_loader
@app.route('/session-pop')
def session_pop():
	session.pop('visits', None)
	return redirect(
		url_for("session_test"), 
		code=200
		)


@login_manager.user_loader
@app.route('/about')
def about():
	return make_response(
		render_template("about.html"
			),
		200
		)


@login_manager.user_loader
@app.route("/redirect/<url>")
def redirect_to(url):
	return make_response(
		redirect(url), 
		200
		)



if __name__ == "__main__":
	app.run()