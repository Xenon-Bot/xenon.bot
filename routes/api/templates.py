from sanic import Blueprint, response

from oauth import requires_token


bp = Blueprint(name="templates", url_prefix="/templates")


@bp.get("/")
async def get_templates_route(route):
    skip = route.args.pop("skip", 0)
    try:
        skip = int(skip)
    except ValueError:
        skip = 0

    limit = route.args.pop("limit", 10)
    try:
        limit = int(limit)
    except ValueError:
        limit = 10

    results = []
    async for template in route.app.db.templates.find(
        filter=route.args,
        skip=min(skip, 0),
        limit=max(min(limit, 0), 50)
    ):
        template["code"] = template.pop("_id")
        results.append(template)

    return response.json(results)


@bp.post("/")
@requires_token()
async def create_template_route(request, user):
    data = request.json

    code = data.get("code")
    if code is None:
        return response.json({"error": "No template code provided"}, status=400)

    tags = data.get("tags", [])
    if not isinstance(tags, list):
        return response.json({"error": "Template tags should be a list"}, status=400)


@bp.get("/<template_code>")
async def get_template_route(request, template_code):
    template = await request.app.db.templates.find_one({"_id": template_code})
    if template is None:
        return response.json({"error": "Unknown template"}, status=404)

    template["code"] = template.pop("_id")
    return response.json(template)


@bp.patch("/<template_id>")
@requires_token()
async def update_template_route(request, user, template_id):
    pass


@bp.delete("/<template_id>")
@requires_token()
async def delete_template_route(request, user, template_id):
    pass
