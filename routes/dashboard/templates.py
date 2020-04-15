from sanic import Blueprint

from helpers import template


bp = Blueprint("dashboard.templates", url_prefix="/templates")


@bp.get("/")
@template("dashboard/templates.jinja2")
async def templates_page(request):
    return {}
