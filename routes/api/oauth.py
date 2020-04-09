from sanic import Blueprint, response
import aiohttp

from oauth import requires_token
import helpers


bp = Blueprint(name="oauth", url_prefix="/oauth")


@bp.post("/token")
@helpers.requires_body("access_token", "expires_in", "scope", "token_type")
async def exchange_token_route(request):
    data = request.json

    try:
        user = await request.app.oauth_user(token=data["access_token"])
    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            return response.json({"error": "Invalid Token"}, status=400)

        else:
            return response.json({"error": e.message}, status=e.status)

    await request.app.store_oauth(user["id"], data)
    jwt_token = helpers.encode_jwt(request.app, {"user_id": user["id"]})

    return response.json({"token": jwt_token})


@bp.get("/token")
@requires_token
async def get_token_route(request, user):
    oauth_data = await request.app.get_oauth(user.id)
    if oauth_data is None:
        raise response.json({"error": "Oauth token expired. The JWT token is still safe to use."}, status=401)

    return response.json(oauth_data)


@bp.delete("/token")
@requires_token
async def delete_token_route(request, user):
    await request.app.delete_oauth(user.id)
    return response.empty()
