from sanic import Blueprint, response
from stay_fast import *
from helpers import *


bp = Blueprint(name="api.backups", url_prefix="/backups")


@bp.get("/ids")
@ratelimit(limit=5, seconds=5)
async def get_ids(request):
    query = request.args
    translator = await request.app.db.id_translators.find_one({
        "source_id": query.get("source"),
        "target_id": query.get("target")
    })

    if translator is not None:
        return response.json(translator["ids"])

    else:
        return response.json({"error": "No id translator found"}, status=404)

