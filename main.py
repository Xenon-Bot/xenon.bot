from sanic import Sanic
import jinja2
from motor.motor_asyncio import AsyncIOMotorClient
import aioredis
import aiohttp
import pymongo

import routes
import helpers


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

        self.session = None

        self.register_listener(self.setup, "before_server_start")
        self.register_listener(self.teardown, "after_server_stop")

    async def setup(self, _, loop):
        self.mongo = AsyncIOMotorClient()
        self.db = self.mongo.xenon
        await self.db.new_templates.create_index([("_id", pymongo.TEXT), ("description", pymongo.TEXT)])

        self.session = aiohttp.ClientSession(loop=loop)
        self.redis = await aioredis.create_redis_pool("redis://localhost", loop=loop)

    async def teardown(self, _, loop):
        await self.session.close()
        self.redis.close()
        await self.redis.wait_closed()


app = App(name="xenon.bot", load_env="APP_", strict_slashes=False)

app.config.PROXIES_COUNT = 2

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, access_log=True, debug=True, auto_reload=False)
