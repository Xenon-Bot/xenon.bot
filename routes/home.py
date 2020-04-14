from sanic import Blueprint

from helpers import template

bp = Blueprint("home")

EXAMPLES = [
    {
        "img": "/static/img/examples/backup_create.jpg",
        "title": "Create Backups",
        "text": "Backups are used to save the current state of your server including roles, channels, "
                "bans and even more with <a href=\"#tiers\" class=\"text-secondary\">premium</a>. Backups are bind to "
                "your account and can be loaded on any server where you have administrator permissions.<br/>"
                "Create a backup with <code>x!backup create</code>."
    },
    {
        "img": "/static/img/examples/backup_interval.jpg",
        "title": "Backup Interval",
        "text": "In addition to manual backups, you can enable the backup interval. It will automatically create "
                "backup in the set interval. Ony the last interval backup of each server is kept unless you have "
                "<a href=\"#tiers\" class=\"text-secondary\">premium</a>.<br/>"
                "Enable the backup interval with <code>x!backup interval 24h</code>."
    },
    {
        "img": "/static/img/examples/template_load.jpg",
        "title": "Load a Template",
        "text": "Templates are the public counterpart to backups. A template can be loaded by everyone and doesn't "
                "contain any private information. Users can use templates to share their server setups with others."
                "<br/>Use <code>x!template load starter</code> to load the starter template."
    },
    {
        "img": "/static/img/examples/sync_messages.jpg",
        "title": "Transfer Messages",
        "text": "With <a href=\"#tiers\" class=\"text-secondary\">premium</a> you can transfer messages using full server backups, per channel "
                "chatlogs or message synchronization. The transferred messages appear with the same content, username "
                "and avatar as the original ones. Only a small \"bot\" badge identifies them as transferred ones."
    },
]

FEATURES = [
    {
        "icon": "save",
        "title": "Manual Backups",
        "text": "Create a backup of you server and load whenever you want"
    },
    {
        "icon": "update",
        "title": "Backup Interval",
        "text": "Enable the backup interval to create automatic backups in a set interval"
    },
    {
        "icon": "amp_stories",
        "title": "Templates",
        "text": "Take advantage of many public templates to create your new discord server in seconds"
    },
    {
        "icon": "sync_alt",
        "title": "Synchronization",
        "text": "Connect multiple channels and transfer all new messages between them"
    },
]

QUESTIONS = [
    {
        "question": "How do I add Xenon to my server?",
        "answer": "You can use this link to invite Xenon to your server: "
                  "<a href=\"/invite\" class=\"text-secondary\">https://xenon.bot/invite</a>"
    },
    {
        "question": "How can I create and load a backup?",
        "answer": "You can create a backup of your discord server using the <code>x!backup create</code> command. "
                  "You will get the command to load the backup after it was created.<br/>"
                  "Keep in mind that you need administrator permissions to create or load a backup."
    },
    {
        "question": "Can I load backups from a different discord account?",
        "answer": "No. Backups are linked to the discord account of the creator and can't be used by anyone else. "
                  "There is no way to transfer a backup from one user to another."
    },
    {
        "question": "My backup is missing but I didn't delete it?!",
        "answer": "Backups that were created before 11/04/19 can no longer be accessed. "
                  "There was a long migration period.<br/>"
                  "Please also keep in mind that a backup can only be loaded with the discord account that create it."
    },
    {
        "question": "Where can I find a list of my backups?",
        "answer": "You can use <code>x!backup list</code> to get a list of your backups."
    },
    {
        "question": "How can I create and load a template?",
        "answer": "WIP"
    },
    {
        "question": "What is the best template for me?",
        "answer": "WIP"
    }
]

TIERS = [
    {
        "img": "/static/img/xenon.jpg",
        "name": "Xenon",
        "features": [
            {
                "value": True,
                "text": "Backup channels and roles"
            },
            {
                "value": True,
                "text": "Up to 25 backups"
            },
            {
                "value": True,
                "text": "Keep 1 interval backup per server"
            },
            {
                "value": False,
                "text": "Save role assignments and nicknames"
            },
            {
                "value": False,
                "text": "Save messages"
            },
            {
                "value": False,
                "text": "Synchronize messages and bans"
            }
        ],
        "button": '<a class="btn btn-outline-primary my-sm-0" href="/invite">'
                  '<span class="align-middle">Invite for Free</span></a>'
    },
    {
        "img": "/static/img/premium.jpg",
        "name": "Premium 1",
        "features": [
            {
                "value": True,
                "text": "Backup channels and roles"
            },
            {
                "value": True,
                "text": "Up to 50 backups"
            },
            {
                "value": True,
                "text": "Keep 2 interval backup per server"
            },
            {
                "value": True,
                "text": "Save role assignments and nicknames"
            },
            {
                "value": True,
                "text": "Save 50 messages per channel"
            },
            {
                "value": True,
                "text": "Synchronize messages and bans"
            }
        ],
        "button": '<a class="btn btn-outline-secondary my-sm-0" target="_blank"'
                  'href="https://www.patreon.com/join/merlinfuchs/checkout?rid=4409325">'
                  '<span class="align-middle">Buy for 5$/m</span></a>'
    },
    {
        "img": "/static/img/premium.jpg",
        "name": "Premium 2",
        "features": [
            {
                "value": True,
                "text": "Backup channels and roles"
            },
            {
                "value": True,
                "text": "Up to 100 backups"
            },
            {
                "value": True,
                "text": "Keep 4 interval backup per server"
            },
            {
                "value": True,
                "text": "Save role assignments and nicknames"
            },
            {
                "value": True,
                "text": "Save 100 messages per channel"
            },
            {
                "value": True,
                "text": "Synchronize messages and bans"
            }
        ],
        "button": '<a class="btn btn-outline-secondary my-sm-0" target="_blank"'
                  'href="https://www.patreon.com/join/merlinfuchs/checkout?rid=4837411">'
                  '<span class="align-middle">Buy for 10$/m</span></a>'
    },
    {
        "img": "/static/img/premium.jpg",
        "name": "Premium 3",
        "features": [
            {
                "value": True,
                "text": "Backup channels and roles"
            },
            {
                "value": True,
                "text": "Up to 250 backups"
            },
            {
                "value": True,
                "text": "Keep 8 interval backup per server"
            },
            {
                "value": True,
                "text": "Save role assignments and nicknames"
            },
            {
                "value": True,
                "text": "Save 250 messages per channel"
            },
            {
                "value": True,
                "text": "Synchronize messages and bans"
            }
        ],
        "button": '<a class="btn btn-outline-secondary my-sm-0" target="_blank"'
                  'href="https://www.patreon.com/join/merlinfuchs/checkout?rid=3820460">'
                  '<span class="align-middle">Buy for 15$/m</span></a>'
    }
]


@bp.route("/")
@template("index.jinja2")
async def home_page(request):
    return {
        "examples": EXAMPLES,
        "features": FEATURES,
        "questions": QUESTIONS,
        "tiers": TIERS
    }


@bp.route("/status")
@template("status.jinja2")
async def status_page(request):
    return {}


@bp.route("/legal/privacy")
@template("privacy.jinja2")
async def privacy_page(request):
    return {}


@bp.route("/legal/cookies")
@template("cookies.jinja2")
async def terms_page(request):
    return {}
