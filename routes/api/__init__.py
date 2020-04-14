from sanic import Blueprint

from . import templates, oauth, general


bp = Blueprint.group(general.bp, oauth.bp, templates.bp, url_prefix="/api")
