from sanic import response
import jwt
from datetime import datetime, timedelta

import helpers


API_ENDPOINT = "https://discordapp.com/api"


class AuthUser:
    def __init__(self, user_id, token_data=None, admin=False):
        self.id = user_id
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        if token_data is not None:
            self.access_token = token_data["a"]
            self.refresh_token = token_data["r"]
            self.expires_at = datetime.fromtimestamp(token_data["e"])

        self.admin = admin


class OAuthMixin:
    async def oauth_request(self, method, endpoint, *, token, **kwargs):
        async with self.session.request(
                method=method,
                url=API_ENDPOINT + endpoint,
                headers={"Authorization": f"Bearer {token}"},
                **kwargs
        ) as resp:
            resp.raise_for_status()
            return await helpers.json_or_text(resp)

    async def token_exchange(self, code):
        async with self.session.post(
            url=API_ENDPOINT + "/oauth2/token",
            data={
                "client_id": self.config.OAUTH_CLIENT_ID,
                "client_secret": self.config.OAUTH_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://xenon.bot/dashboard",
                "scope": "identify"
            }
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    def oauth_get_user(self, *, token):
        return self.oauth_request("GET", "/users/@me", token=token)

    def oauth_get_guilds(self, *, token):
        return self.oauth_request("GET", "/users/@me/guilds", token=token)

    def oauth_get_guilds(self, *, token):
        return self.oauth_request("GET", "/users/@me/guilds", token=token)

    def make_jwt_token(self, user_id, token_data=None):
        data = {"u": user_id}
        if token_data is not None:
            data["t"] = {
                "a": token_data["access_token"],
                "e": (datetime.utcnow() + timedelta(seconds=token_data["expires_in"])).timestamp(),
                "r": token_data["refresh_token"]
            }

        return helpers.encode_jwt(self, data)

    def get_user(self, jwt_token):
        data = helpers.decode_jwt(self, jwt_token)
        return AuthUser(
            user_id=data["u"],
            token_data=data.get("t"),
            admin=data.get("a", False)
        )


def requires_token(admin_only=False, user_only=False):
    def predicate(handler):
        async def wrapper(request, *args, **kwargs):
            jwt_token = request.headers.get("Authorization")
            if jwt_token is None:
                return response.json({"error": "Unauthorized"}, status=401)

            try:
                user = request.app.get_user(jwt_token)
            except jwt.DecodeError:
                return response.json({"error": "Invalid token"}, status=401)

            if user_only and user.access_token is None:
                return response.json({"error": "This endpoint requires a user token"}, status=401)

            # User tokens expire when they access token expires
            if user.expires_at is not None and user.expires_at < datetime.utcnow():
                return response.json({"error": "Token expired"}, status=401)

            if admin_only and not user.admin:
                return response.json({"error": "Admin privileges required"}, status=401)

            return await handler(request, user, *args, **kwargs)

        return wrapper

    return predicate
