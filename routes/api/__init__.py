from sanic import Blueprint

from . import general, templates


bp = Blueprint.group(general.bp, templates.bp, url_prefix="/api")
