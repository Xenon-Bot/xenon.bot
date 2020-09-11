from sanic import response
import jwt
from datetime import datetime

from helpers import encode_jwt, decode_jwt


__all__ = (
    "TokenType",
    "generate_bot_token",
    "requires_bot_token"
)


class TokenType:
    BOT = 0
    USER = 1


def generate_bot_token(app, bot_id):
    return encode_jwt(app, {"t": TokenType.BOT, "id": bot_id})


def requires_bot_token():
    def predicate(handler):
        async def wrapper(request, *args, **kwargs):
            jwt_token = request.headers.get("Authorization")
            if jwt_token is None:
                return response.json({"error": "Unauthorized"}, status=401)

            try:
                data = decode_jwt(request.app, jwt_token)
            except jwt.DecodeError:
                return response.json({"error": "Invalid token"}, status=401)

            if data["t"] != TokenType.BOT:
                return response.json({"error": "This endpoint requires a bot token"}, status=401)

            return await handler(request, data["id"], *args, **kwargs)

        return wrapper

    return predicate
