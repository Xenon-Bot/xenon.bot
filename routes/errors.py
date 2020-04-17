from sanic import Blueprint, exceptions

from helpers import template


bp = Blueprint("errors")


@bp.exception(exceptions.NotFound)
@template("errors/404.jinja2")
async def handler(request, exception):
    return {}


@bp.exception(exceptions.ServerError)
@template("errors/500.jinja2")
async def handler(request, exception):
    return {}
