from flask import Flask, url_for, render_template, request, make_response, redirect, session

app = Flask(
	__name__, 
	template_folder = "templates", 
	static_folder = "static"
)

app.secret_key = "super secret key"
app.debug = True


def has_no_empty_params(rule):
	defaults = rule.defaults if rule.defaults is not None else ()
	arguments = rule.arguments if rule.arguments is not None else ()
	return len(defaults) >= len(arguments)


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