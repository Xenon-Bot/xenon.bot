from sanic import Blueprint, response
import aiohttp

from oauth import requires_token
import helpers


bp = Blueprint(name="api.oauth", url_prefix="/oauth")


@bp.post("/token")
@helpers.requires_body("access_token")
async def exchange_token_route(request):
    data = request.json
    access_token = data["access_token"]

    try:
        user = await request.app.oauth_user(token=access_token)
    except aiohttp.ClientResponseError as e:
        if e.status == 401:
            return response.json({"error": "Invalid Token"}, status=400)

        else:
            return response.json({"error": e.message}, status=e.status)

    jwt_token = request.app.make_jwt_token(user["id"], access_token)
    return response.json({"token": jwt_token})


@bp.get("/token")
@requires_token()
async def get_token_route(request, user):
    return response.json({"access_token": user.access_token})
