from sanic import Blueprint, response

from stay_fast import *
from auth import *
from helpers import *


bp = Blueprint(name="api.templates", url_prefix="/templates")


@bp.get("/<template_id>/bots")
@ratelimit(limit=30, seconds=10, level=RequestBucket.TOKEN)
@cache_response(minutes=1)
async def set_settings(request, template_id):
    template = await request.app.mongo.dtpl.templates.find_one({"_id": template_id}, projection=("bots",))
    if template is None:
        return response.json({"error": "Unknown template"}, status=404)

    return response.json({"bots": template.get("bots", [])})


@bp.post("/<template_id>/bots")
@requires_bot_token()
@ratelimit(limit=30, seconds=10, level=RequestBucket.TOKEN)
@requires_body("user")
async def set_settings(request, bot_id, template_id):
    user_id = request.json["user"]
    template = await request.app.mongo.dtpl.templates.find_one({"_id": template_id}, projection=("creator_id",))
    if template is None:
        return response.json({"error": "Unknown template"}, status=404)

    if template["creator_id"] != user_id:
        return response.json({"error": "User is not the creator"}, status=403)

    await request.app.mongo.dtpl.templates.update_one({"_id": template_id}, {"$addToSet": {"bots": bot_id}})
    return response.json({})


@bp.delete("/<template_id>/bots")
@requires_bot_token()
@ratelimit(limit=30, seconds=10, level=RequestBucket.TOKEN)
@requires_body("user")
async def delete_settings(request, bot_id, template_id):
    user_id = request.json["user"]
    template = await request.app.mongo.dtpl.templates.find_one({"_id": template_id}, projection=("creator_id",))
    if template is None:
        return response.json({"error": "Unknown template"}, status=404)

    if template["creator_id"] != user_id:
        return response.json({"error": "User is not the creator"}, status=403)

    await request.app.mongo.dtpl.templates.update_one({"_id": template_id}, {"$pull": {"bots": bot_id}})
    return response.json({})
