from sanic import Blueprint, response

bp = Blueprint("links")

INVITE_LINK = "https://discordapp.com/oauth2/authorize?client_id=416358583220043796&scope=bot&permissions=8"
DISCORD_LINK = "https://discord.gg/5GmAsPs"
DOCS_LINK = "https://docs.xenon.bot"
PATREON_LINK = "https://www.patreon.com/merlinfuchs"


@bp.route("/invite")
async def invite_link(request):
    return response.redirect(INVITE_LINK, status=307)


@bp.route("/discord")
async def discord_link(request):
    return response.redirect(DISCORD_LINK, status=307)


@bp.route("/support")
async def support_link(request):
    return response.redirect(DISCORD_LINK, status=307)


@bp.route("/docs")
async def docs_link(request):
    return response.redirect(DOCS_LINK, status=307)


@bp.route("/docs/<path:path>")
async def docs_link(request, path):
    return response.redirect(DOCS_LINK + "/" + path, status=307)


@bp.route("/patreon")
async def patreon_link(request):
    return response.redirect(PATREON_LINK, status=307)
