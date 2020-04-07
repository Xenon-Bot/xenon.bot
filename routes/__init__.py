from sanic import Blueprint

from . import home


bp = Blueprint.group(home.bp)