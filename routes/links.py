from sanic import Blueprint, response

bp = Blueprint("links")

INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=416358583220043796" \
              "&permissions=8&scope=applications.commands%20bot"
DISCORD_LINK = "https://discord.gg/5GmAsPs"
DOCS_LINK = "https://wiki.xenon.bot"
PATREON_LINK = "https://www.patreon.com/merlinfuchs"
GITHUB_LINK = "https://github.com/Xenon-Bot"
TWITTER_LINK = "https://twitter.com/xenon_bot"
IG_LINK = "https://www.instagram.com/xenon.bot/"


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


@bp.route("/github")
async def github_link(request):
    return response.redirect(GITHUB_LINK, status=307)


@bp.route("/twitter")
async def github_link(request):
    return response.redirect(TWITTER_LINK, status=307)


@bp.route("/instagram")
async def github_link(request):
    return response.redirect(IG_LINK, status=307)


@bp.route("/iv/<backup_id>")
async def backup_invite(request, backup_id):
    backup = await request.app.db.backups.find_one({"_id": backup_id, "const_invite": True}, projection=("invite",))
    if backup is None or backup.get("invite") is None:
        return response.text("Unknown invite. Maybe the creator disabled it.", status=404)

    return response.redirect(f"https://discord.gg/{backup['invite']}")
