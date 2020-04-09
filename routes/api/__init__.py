from sanic import Blueprint

from . import templates, oauth


bp = Blueprint.group(oauth.bp, templates.bp, url_prefix="/api")
