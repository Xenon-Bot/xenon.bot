from sanic import Blueprint, response
import msgpack
import stay_fast


bp = Blueprint(name="general")


@bp.get("/shards")
@stay_fast.ratelimit(limit=5, seconds=5)
@stay_fast.cache_response(minutes=1)
async def shards_route(request):
    shard_count_raw = await request.app.redis.hget("state", "shard_count")

    shard_count = None
    if shard_count_raw is not None:
        shard_count = msgpack.unpackb(shard_count_raw)

    shards_raw = await request.app.redis.hgetall("shards")
    shards = {}
    for shard_id, data in shards_raw.items():
        shards[shard_id.decode("utf-8")] = msgpack.unpackb(data)

    for i in range(shard_count):
        # Fill up offline shards
        if str(i) not in shards.keys():
            shards[str(i)] = None

    return response.json({
        "shard_count": shard_count,
        "shards": shards
    })


@bp.get("/stats")
@stay_fast.ratelimit(limit=5, seconds=5)
@stay_fast.cache_response(minutes=10)
async def stats_route(request):
    guild_count = await request.app.redis.hlen("guilds")
    role_count = await request.app.redis.hlen("roles")
    channel_count = await request.app.redis.hlen("channels")
    shard_count_raw = await request.app.redis.hget("state", "shard_count")

    shard_count = None
    if shard_count_raw is not None:
        shard_count = msgpack.unpackb(shard_count_raw)

    backup_count = await request.app.db.backups.estimated_document_count()
    template_count = await request.app.db.templates.estimated_document_count()

    return response.json({
        "guild_count": guild_count,
        "role_count": role_count,
        "channel_count": channel_count,
        "shard_count": shard_count,
        "backup_count": backup_count,
        "template_count": template_count
    })
