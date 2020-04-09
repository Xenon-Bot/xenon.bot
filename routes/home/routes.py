from sanic import Blueprint

from helpers import template


bp = Blueprint("home")


@bp.route("/")
@template("index.jinja2")
async def home_page(request):
    return {}


@bp.route("/status")
@template("status.jinja2")
async def status_page(request):
    return {}
