from sanic import response

import helpers


API_ENDPOINT = "https://discordapp.com/api"


class AuthUser:
    def __init__(self, user_id, access_token, admin=False):
        self.id = user_id
        self.access_token = access_token
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

    def oauth_get_user(self, *, token):
        return self.oauth_request("GET", "/users/@me", token=token)

    def oauth_get_guilds(self, *, token):
        return self.oauth_request("GET", "/users/@me/guilds", token=token)

    def make_jwt_token(self, user_id, access_token):
        return helpers.encode_jwt(self, {"u": user_id, "t": access_token})

    def get_user(self, jwt_token):
        data = helpers.decode_jwt(self, jwt_token)
        return AuthUser(data["u"], data["t"])


def requires_token(admin=False):
    def predicate(handler):
        async def wrapper(request, *args, **kwargs):
            jwt_token = request.headers.get("Authorization")
            if jwt_token is None:
                return response.json({"error": "Unauthorized"}, status=401)

            user = request.app.get_user(jwt_token)
            if admin and not user.admin:
                return response.json({"error": "Admin privileges required"}, status=401)

            return await handler(request, user, *args, **kwargs)

        return wrapper

    return predicate
