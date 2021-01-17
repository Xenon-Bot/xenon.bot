from sanic import Blueprint, response
import traceback

from auth import TokenType
from helpers import *
from stay_fast import *


bp = Blueprint(name="api.oauth", url_prefix="/oauth")


@bp.post("/exchange")
@ratelimit(limit=3, seconds=5)
@requires_body()
async def invite_callback(req):
    code = req.json.get("code")

    if code is None:
        return response.json({"error": "No code provided"}, status=400)

    config = req.app.config
    try:
        async with req.app.session.post("https://discord.com/api/v8/oauth2/token", data={
            "client_id": config.OAUTH_CLIENT_ID,
            "client_secret": config.OAUTH_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.OAUTH_REDIRECT_URI,
            "scope": "identify"
        }) as resp:
            if resp.status != 200:
                return response.json({"error": f"Token exchange failed {resp.status}"}, status=400)

            data = await resp.json()
            if "guild" in data:
                await req.app.redis.sadd("invites", data["guild"]["id"])

            if "identify" not in data["scope"]:
                return response.json({"error": "Invalid scopes"}, status=400)

            async with req.app.session.get("https://discord.com/api/v8/users/@me", headers={
                "Authorization": f"Bearer {data['access_token']}"
            }) as resp:
                if resp.status == 200:
                    user_data = await resp.json()
                    token = encode_jwt(req.app, {"t": TokenType.USER, "id": user_data["id"]})
                    return response.json({
                        "token": token,
                        "scope": data["scope"],
                        "access_token": data["access_token"]
                    })

    except:
        traceback.print_exc()
        return response.json({"error": "Something went wrong"}, status=400)
