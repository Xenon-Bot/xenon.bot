from sanic import Blueprint

from . import home, api, templates


bp = Blueprint.group(home.bp, api.bp)
