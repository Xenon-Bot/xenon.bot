from sanic import Blueprint

from . import templates, home


bp = Blueprint.group(home.bp, templates.bp, url_prefix="/dashboard")
