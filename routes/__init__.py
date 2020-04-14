from sanic import Blueprint

from . import home, api, templates, links


bp = Blueprint.group(home.bp, api.bp, links.bp)
