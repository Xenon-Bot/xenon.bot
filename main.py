from sanic import Sanic
import jinja2
from motor.motor_asyncio import AsyncIOMotorClient
import aioredis
import aiohttp
import pymongo
import weakref
import asyncio

import routes
import helpers


class RedisSubscriber:
    def __init__(self, redis, loop):
        self.redis = redis
        self.mpsc = aioredis.pubsub.Receiver()
        self.loop = loop
        self.loop.create_task(self.reader())

        self.subscribers = weakref.WeakSet()

    async def reader(self):
        async for channel, msg in self.mpsc.iter():
            for fut in self.subscribers:
                if not fut.done():
                    fut.set_result((channel, msg))

            self.subscribers.clear()

    async def subscribe(self, *channels):
        await self.redis.subscribe(*[self.mpsc.channel(c) for c in channels])
        while self.mpsc.is_active:
            fut = asyncio.Future()
            self.subscribers.add(fut)
            channel, msg = await fut
            if channel.name.decode("utf-8") in channels:
                yield channel, msg

    async def psubscribe(self, *channels):
        await self.redis.psubscribe(*[self.mpsc.pattern(c) for c in channels])
        while self.mpsc.is_active:
            fut = asyncio.Future()
            self.subscribers.add(fut)
            channel, msg = await fut
            if channel.name.decode("utf-8") in channels:
                yield channel, msg


class App(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.blueprint(routes.bp)

        # Static Files
        # Should be served by nginx before reaching Sanic
        self.static("/static", "./static")

        # Templating Engine
        self.jinja2 = jinja2.Environment(
            loader=jinja2.FileSystemLoader("./templates"),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            enable_async=True
        )
        self.jinja2.globals.update({
            "app": self,
            "helpers": helpers
        })

        self.mongo = None
        self.db = None
        self.redis = None
        self.subscriber = None

        self.session = None

        self.register_listener(self.setup, "before_server_start")
        self.register_listener(self.teardown, "after_server_stop")

    async def setup(self, _, loop):
        self.mongo = AsyncIOMotorClient(getattr(self.config, "MONGO_URL", "mongodb://127.0.0.1"))
        self.db = self.mongo.xenon
        await self.db.new_templates.create_index([("_id", pymongo.TEXT), ("description", pymongo.TEXT)])

        self.session = aiohttp.ClientSession(loop=loop)
        self.redis = await aioredis.create_redis_pool(getattr(self.config, "REDIS_URL", "redis://localhost"), loop=loop)
        self.subscriber = RedisSubscriber(self.redis, loop=loop)

    async def teardown(self, _, loop):
        await self.session.close()
        self.redis.close()
        await self.redis.wait_closed()


app = App(name="xenon.bot", load_env="APP_", strict_slashes=False)

app.config.PROXIES_COUNT = 2

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, access_log=True, debug=True, auto_reload=False)
