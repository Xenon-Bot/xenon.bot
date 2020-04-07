from sanic import Blueprint

from helpers import template


bp = Blueprint("home")


@bp.route("/")
@template("index.jinja2")
async def home_route(request):
    return {}
