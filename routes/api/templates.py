from sanic import Blueprint, response
import pymongo.errors

from oauth import requires_token
from helpers import requires_body
import stay_fast


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

    tags = query.get("tags")
    if tags is not None:
        filter["tags"] = tags

    results = []
    async for template in route.app.db.templates.find(
        filter=filter,
        skip=min(skip, 0),
        limit=max(min(limit, 0), 50)
    ):
        template["code"] = template.pop("_id")
        results.append(template)

    return response.json(results)


@bp.post("/")
@stay_fast.ratelimit(limit=2, seconds=10)
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

    try:
        await request.app.db.templates.insert_one({
            "_id": code,
            "creator": user.id,
            "name": name,
            "description": description,
            "tags": tags,
            "external": True
        })
    except pymongo.errors.DuplicateKeyError:
        return response.json({"error": "This template was already added"}, status=400)

    return response.empty()


@bp.get("/<template_code>")
@stay_fast.ratelimit(limit=5, seconds=5)
@requires_token()
async def get_template_route(request, user, template_code):
    template = await request.app.db.templates.find_one({"_id": template_code})
    if template is None:
        return response.json({"error": "Unknown template"}, status=404)

    template["code"] = template.pop("_id")
    return response.json(template)


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

    result = await request.app.templates.update_one({"_id": template_id, "creator": user.id}, to_update)
    if result.matched_count == 0:
        return response.json({"error": "This template does either not exist or you are not the creator"})

    return response.empty()


@bp.delete("/<template_id>")
@stay_fast.ratelimit(limit=5, seconds=10)
@requires_token()
async def delete_template_route(request, user, template_id):
    result = await request.app.templates.delete_one({"_id": template_id, "creator": user.id})
    if result.deleted_count == 0:
        return response.json({"error": "This template does either not exist or you are not the creator"})

    return response.empty()
