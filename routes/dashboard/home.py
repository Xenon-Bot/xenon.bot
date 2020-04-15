from sanic import Blueprint, response

from helpers import template


bp = Blueprint("dashboard.home")


@bp.get("/")
async def templates_page(request):
    return response.redirect("/dashboard/templates", status=307)
