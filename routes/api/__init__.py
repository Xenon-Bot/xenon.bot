from sanic import Blueprint

from . import general, backups


bp = Blueprint.group(general.bp, backups.bp, url_prefix="/api")
