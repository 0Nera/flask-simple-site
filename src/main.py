from flask import Flask, url_for, render_template, request, make_response, redirect

app = Flask(
	__name__, 
	template_folder = "templates", 
	static_folder = "static"
)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/')
def index():
    return make_response("Hello World! Your IP is {} and you are using {}<br><a href='./site-map'>Sitemap</a>".format(request.remote_addr, request.user_agent), 200)


@app.route("/redirect/<url>")
def redirect_to(url):
    return make_response(redirect(url), 200)





@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return make_response(render_template("all_links.html", links=links), 200)


if __name__ == "__main__":
    app.run(
        debug=True
        )