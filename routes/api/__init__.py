from sanic import Blueprint

from . import general, templates, oauth


bp = Blueprint.group(general.bp, templates.bp, oauth.bp, url_prefix="/api")
