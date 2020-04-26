from sanic import Blueprint, response
import pymongo.errors
from datetime import datetime

from oauth import requires_token
from helpers import requires_body
import stay_fast


VALID_TAGS = ("gaming", "school", "roleplay", "development", "support", "community", "clan")


bp = Blueprint("api.templates", url_prefix="/templates")


@bp.get("/")
@stay_fast.ratelimit(limit=5, seconds=5)
@requires_token()
async def get_templates_route(route, user):
    query = route.args

    skip = query.get("skip", 0)
    try:
        skip = int(skip)
    except ValueError:
        skip = 0

    limit = query.get("limit", 10)
    try:
        limit = int(limit)
    except ValueError:
        limit = 10

    filter = {}
    search = query.get("search")
    if search is not None:
        filter["$text"] = {"$search": search}

    tag = query.get("tag")
    if tag is not None:
        filter["tags"] = tag

    sort = query.get("sort", "views")
    direction = pymongo.DESCENDING
    if sort.startswith("-"):
        sort = sort[1:]
        direction = pymongo.ASCENDING

    results = []
    async for template in route.app.db.new_templates.find(
        filter=filter,
        skip=max(skip, 0),
        limit=min(max(limit, 0), 50),
        sort=[(sort, direction)]
    ):
        if template.get("internal"):
            template.pop("serialized_source_guild", None)

        template["code"] = template.pop("_id")
        results.append(template)

    return response.json(results)


@bp.post("/")
@stay_fast.ratelimit(limit=2, seconds=30)
@requires_token()
@requires_body("code", "name", "description", "tags")
async def create_template_route(request, user):
    data = request.json

    code = data["code"]
    name = data["name"]
    if len(name) < 5:
        return response.json({"error": "Template name should be at least 5 characters long"}, status=400)

    description = data["description"]
    if len(description) < 10:
        return response.json({"error": "Template description should be at least 10 characters long"}, status=400)

    tags = data["tags"]
    if not isinstance(tags, list):
        return response.json({"error": "Template tags should be a list"}, status=400)

    timestamp = datetime.utcnow()
    try:
        await request.app.db.new_templates.insert_one({
            "_id": code,
            "creator_id": user.id,
            "name": name,
            "description": description,
            "tags": tags,
            "views": 0,
            "usage_count": 0,
            "upvotes": [],
            "upvote_count": 0,
            "created_at": timestamp,
            "updated_at": timestamp,
            "internal": False
        })
    except pymongo.errors.DuplicateKeyError:
        return response.json({"error": "This template was already added"}, status=400)

    return response.empty()


@bp.get("/tags")
@stay_fast.ratelimit(limit=5, seconds=5)
@requires_token()
async def get_tags_route(request, user):
    return response.json(list(VALID_TAGS))


@bp.get("/<template_code>")
@stay_fast.ratelimit(limit=10, seconds=5)
@requires_token()
async def get_template_route(request, user, template_code):
    template = await request.app.db.new_templates.find_one({"_id": template_code})
    if template is None:
        return response.json({"error": "Unknown template"}, status=404)

    template["code"] = template.pop("_id")
    if template.get("internal"):
        template.pop("serialized_source_guild", None)

    return response.json(template)


@bp.get("/<template_code>/data")
@stay_fast.ratelimit(limit=5, seconds=5)
@requires_token()
async def get_template_data_route(request, user, template_code):
    template = await request.app.db.new_templates.find_one_and_update({"_id": template_code}, {"$inc": {"views": 1}})
    if template is None or not template.get("internal"):
        # External templates can be fetched from discord directly
        return response.redirect(f"https://discordapp.com/api/v6/guilds/templates/{template_code}", status=307)

    template["code"] = template.pop("_id")
    return response.json(template)


@bp.post("/<template_id>/upvote")
@stay_fast.ratelimit(limit=2, seconds=10)
@requires_token()
async def upvote_template_route(request, user, template_id):
    await request.app.db.new_templates.update_one({"_id": template_id}, {
        "$addToSet": {"upvotes": user.id},
        "$inc": {"upvote_count": 1}
    })
    return response.empty()


@bp.patch("/<template_id>")
@stay_fast.ratelimit(limit=2, seconds=10)
@requires_token()
async def update_template_route(request, user, template_id):
    data = request.json
    to_update = {}

    name = data.get("name")
    if name is not None:
        if len(name) < 5:
            return response.json({"error": "Template name should be at least 5 characters long"}, status=400)

        to_update["name"] = name

    description = data.get("description")
    if description is not None:
        if len(description) < 10:
            return response.json({"error": "Template description should be at least 10 characters long"}, status=400)

        to_update["description"] = description

    tags = data.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            return response.json({"error": "Template tags should be a list"}, status=400)

        to_update["tags"] = tags

    result = await request.app.db.new_templates.update_one({"_id": template_id, "creator": user.id}, {"$set": to_update})
    if result.matched_count == 0:
        return response.json({"error": "This template does either not exist or you are not the creator"})

    return response.empty()


@bp.delete("/<template_id>")
@stay_fast.ratelimit(limit=5, seconds=10)
@requires_token()
async def delete_template_route(request, user, template_id):
    result = await request.app.db.new_templates.delete_one({"_id": template_id, "creator": user.id})
    if result.deleted_count == 0:
        return response.json({"error": "This template does either not exist or you are not the creator"})

    return response.empty()
