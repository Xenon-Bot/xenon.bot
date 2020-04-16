from sanic import Blueprint, response

from helpers import template


bp = Blueprint("dashboard.home")


@bp.get("/")
@template("dashboard/home.jinja2")
async def home_page(request):
    return {}


@bp.get("/login")
async def login_redirect(request):
    return response.redirect("https://discordapp.com/oauth2/authorize?client_id=416358583220043796&redirect_uri=https%3A%2F%2Fxenon.bot%2Fdashboard&response_type=code&scope=identify%20guilds")
