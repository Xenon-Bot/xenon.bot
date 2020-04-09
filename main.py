from sanic import Sanic
import jinja2
from motor.motor_asyncio import AsyncIOMotorClient
import aioredis
import aiohttp

import routes
import helpers
from oauth import OAuthMixin


class App(Sanic, OAuthMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.blueprint(routes.bp)

        # Static Files
        # Should be served by nginx before reaching Sanic
        self.static("/static", "./static")
        self.static("/dashboard", "./dashboard")

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

        self.db = AsyncIOMotorClient()
        self.redis = None

        self.session = None

        self.register_listener(self.setup_redis, "before_server_start")
        self.register_listener(self.setup_session, "before_server_start")

    async def setup_redis(self, _, loop):
        self.redis = await aioredis.create_redis_pool("redis://localhost", loop=loop)

    async def setup_session(self, _, loop):
        self.session = aiohttp.ClientSession(loop=loop)


app = App(name="xenon.bot", load_env="APP_", strict_slashes=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, access_log=True, debug=True)
