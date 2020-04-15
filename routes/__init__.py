from sanic import Blueprint

from . import home, api, dashboard, links


bp = Blueprint.group(home.bp, api.bp, dashboard.bp, links.bp)
