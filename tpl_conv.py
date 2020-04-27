from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import xenon_worker as wkr


from routes.api.templates import VALID_TAGS


async def convert_templates():
    db = AsyncIOMotorClient().xenon
    async for template in db.templates.find():
        data = template["data"]

        guessed_tags = []
        for tag in VALID_TAGS:
            if tag in template["name"].lower() or tag in template["description"].lower():
                guessed_tags.append(tag)

        channels = []

        text_channels = sorted(
            filter(lambda c: c["type"] == wkr.ChannelType.GUILD_TEXT.value, data["channels"]),
            key=lambda c: c["position"]
        )
        voice_channels = sorted(
            filter(lambda c: c["type"] == wkr.ChannelType.GUILD_VOICE.value, data["channels"]),
            key=lambda c: c["position"]
        )
        ctg_channels = sorted(
            filter(lambda c: c["type"] == wkr.ChannelType.GUILD_CATEGORY.value, data["channels"]),
            key=lambda c: c["position"]
        )

        for channel in filter(lambda c: c.get("parent_id") is None, text_channels):
            channels.append(channel)

        for channel in filter(lambda c: c.get("parent_id") is None, voice_channels):
            channels.append(channel)

        for ctg in ctg_channels:
            channels.append(ctg)
            for channel in filter(lambda c: c.get("parent_id") == ctg["id"], text_channels):
                channels.append(channel)

            for channel in filter(lambda c: c.get("parent_id") == ctg["id"], voice_channels):
                channels.append(channel)

        print(channels)

        await db.new_templates.replace_one({"_id": template["_id"]}, {
            "_id": template["_id"],
            "name": template["name"],
            "description": template.get("description", ""),
            "creator_id": template["creator"],
            "internal":  True,
            "upvotes": [],
            "upvote_count": 0,
            "views": template["uses"],
            "usage_count": template["uses"],
            "created_at": template["timestamp"],
            "updated_at": template["timestamp"],
            "source_guild_id": data["id"],
            "tags": guessed_tags,
            "is_dirty": None,
            "serialized_source_guild": {
                "name": data["name"],
                "description": data.get("description"),
                "region": "eu-central",
                "verification_level": data.get("verification_level", 0),
                "default_message_notifications": data.get("default_message_notifications", 0),
                "explicit_content_filter": data.get("explicit_content_filter", 0),
                "preferred_locale": data.get("preferred_locale"),
                "afk_timeout": data.get("afk_timeout"),
                "afk_channel_id": None,
                "system_channel_id": None,
                "system_channel_flags": 0,
                "icon_hash": data.get("icon"),
                "roles": [
                    {
                        "id": str(id + 1),
                        "name": role["name"],
                        "permissions": role["permissions"],
                        "color": role["color"],
                        "hoist": role.get("hoist", False),
                        "mentionable": role.get("mentionable", False)
                    }
                    for id, role in enumerate(sorted(data["roles"], key=lambda r: r["position"]))
                ],
                "channels": channels
            }
        }, upsert=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(convert_templates())
