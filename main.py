from sanic import Sanic
import jinja2

import routes


app = Sanic(name="xenon.bot", load_env="APP_", strict_slashes=False)
app.blueprint(routes.bp)
app.static("/static", "./static")

# Should be served by nginx before reaching Sanic
app.static("/dashboard", "./dashboard")


app.jinja2 = jinja2.Environment(
    loader=jinja2.FileSystemLoader("./templates"),
    autoescape=jinja2.select_autoescape(['html', 'xml']),
    enable_async=True
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, access_log=True, debug=True)
