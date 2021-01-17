from sanic import Blueprint, response
import traceback

from helpers import template

bp = Blueprint("oauth", url_prefix="/oauth")


@bp.get("/invited")
@template("oauth/invited.jinja2")
async def invite_callback(req):
    code = req.args.get("code")
    permissions = req.args.get("permissions", "0")
    invited = "guild_id" in req.args
    try:
        admin = int(permissions) & 8 == 8
    except ValueError:
        admin = False

    if code is None:
        return {"admin": admin, "invited": invited}

    config = req.app.config
    try:
        async with req.app.session.post("https://discord.com/api/v8/oauth2/token", data={
            "client_id": config.OAUTH_CLIENT_ID,
            "client_secret": config.OAUTH_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.OAUTH_INVITED_URI
        }) as resp:
            if resp.status != 200:
                return {"admin": admin, "invited": invited}

            data = await resp.json()
            if "guild" in data:
                await req.app.redis.sadd("invites", data["guild"]["id"])

            return {
                "guild": data.get("guild"),
                "admin": admin,
                "slash_commands": "applications.commands" in data.get("scope"),
                "invited": invited
            }
    except:
        traceback.print_exc()
        return {"admin": admin}


@bp.get("/callback")
@template("oauth/callback.jinja2")
async def invite_callback(req):
    return {}


@bp.get("/login")
async def invite_callback(req):
    return response.redirect(
        "https://discord.com/api/oauth2/authorize?client_id=416358583220043796"
        "&redirect_uri=https%3A%2F%2Fxenon.bot%2Foauth%2Fcallback&response_type=code&scope=identify",
        status=302
    )
