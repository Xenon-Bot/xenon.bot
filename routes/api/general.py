from sanic import Blueprint, response
import msgpack
import json

from stay_fast import *
from auth import *


bp = Blueprint(name="api.general")


@bp.get("/shards")
@ratelimit(limit=5, seconds=5)
@cache_response(minutes=1)
async def shards_route(request):
    shard_count_raw = await request.app.redis.hget("state", "shard_count")

    shard_count = None
    if shard_count_raw is not None:
        shard_count = msgpack.unpackb(shard_count_raw)

    shards = {}
    if shard_count is not None:
        shards_raw = await request.app.redis.mget(*[f"shards:{i}" for i in range(shard_count)])
        shards = {
            str(i): msgpack.unpackb(data) if data is not None else None
            for i, data in enumerate(shards_raw)
        }

    return response.json({
        "shard_count": shard_count,
        "shards": shards
    })


@bp.get("/stats")
@ratelimit(limit=5, seconds=5)
@cache_response(minutes=10)
async def stats_route(request):
    guild_count_raw = await request.app.redis.hget("state", "guild_count")
    shard_count_raw = await request.app.redis.hget("state", "shard_count")

    shard_count = None
    if shard_count_raw is not None:
        shard_count = msgpack.unpackb(shard_count_raw)

    guild_count = None
    if guild_count_raw is not None:
        guild_count = msgpack.unpackb(shard_count_raw)

    backup_count = await request.app.db.backups.estimated_document_count()
    template_count = await request.app.mongo.dtpl.templates.estimated_document_count()

    return response.json({
        "guild_count": guild_count,
        "shard_count": shard_count,
        "backup_count": backup_count,
        "template_count": template_count
    })


@bp.websocket("/loaders/ws")
@requires_bot_token()
@ratelimit(limit=1, seconds=1, level=RequestBucket.TOKEN)
async def ws_loaders(request, _, ws):
    async for _, msg in request.app.subscriber.psubscribe("loaders:*"):
        event = msg[0].decode("utf-8")[len("loaders:"):]
        data = msgpack.unpackb(msg[1])
        await ws.send(json.dumps({
            "event": event,
            "data": data
        }))


@bp.get("/mappers")
@requires_bot_token()
@ratelimit(limit=30, seconds=10, level=RequestBucket.TOKEN)
@cache_response(respect_query=True, minutes=1)
async def get_ids(request, _):
    query = request.args
    source_id = query.get("source")
    target_id = query.get("target")

    backup_id = query.get("backup")
    if backup_id is not None:
        backup = await request.app.db.backups.find_one({"_id": backup_id}, projection={"data.id": True})
        if backup is not None:
            source_id = backup["data"]["id"]

    translator = await request.app.db.id_translators.find_one({"source_id": source_id, "target_id": target_id})

    if translator is not None:
        del translator["_id"]
        return response.json(translator)

    else:
        return response.json({"error": "No id translator found"}, status=404)
