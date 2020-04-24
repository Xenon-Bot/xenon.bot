from sanic import Blueprint, response

from helpers import template


bp = Blueprint("dashboard", url_prefix="/dashboard")


@bp.get("/")
async def home_page(request):
    url = "/dashboard/templates"
    code = request.args.get("code")
    if code is not None:
        url += "?code=" + code

    return response.redirect(url)


@bp.get("/login")
async def login_redirect(request):
    return response.redirect("https://discordapp.com/oauth2/authorize?client_id=416358583220043796"
                             "&redirect_uri=https%3A%2F%2Fxenon.bot%2Fdashboard"
                             "&response_type=code&scope=identify%20guilds")


@bp.get("/templates")
@template("dashboard/templates.jinja2")
async def templates_page(request):
    return {}


@bp.get("/embedg")
@template("dashboard/embedg.jinja2")
async def templates_page(request):
    return {}
