from sanic import Blueprint

from . import home, api, links, errors, oauth


bp = Blueprint.group(home.bp, api.bp, links.bp, errors.bp, oauth.bp)
