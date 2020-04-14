from sanic import Blueprint

from helpers import template

bp = Blueprint("home")

EXAMPLES = [
    {
        "img": "/static/img/examples/backup_create.jpg",
        "title": "Create Backups",
        "text": ""
    },
    {
        "img": "/static/img/examples/backup_interval.jpg",
        "title": "Backup Interval",
        "text": ""
    },
    {
        "img": "/static/img/examples/template_load.jpg",
        "title": "Load a Template",
        "text": ""
    },
    {
        "img": "/static/img/examples/sync_messages.jpg",
        "title": "Transfer Messages",
        "text": ""
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
        "text": "Create a backup of you server and load whenever you want"
    },
    {
        "icon": "amp_stories",
        "title": "Templates",
        "text": "Create a backup of you server and load whenever you want"
    },
    {
        "icon": "sync_alt",
        "title": "Synchronization",
        "text": "Create a backup of you server and load whenever you want"
    },
]

QUESTIONS = [
    {
        "question": "How do I invite Xenon?",
        "answer": "Click here to invite Xenon."
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
            }
        ],
        "button": '<a class="btn btn-outline-primary my-sm-0" href="/invite"><span class="align-middle">Invite for Free</span></a>'
    },
    {
        "img": "/static/img/premium.jpg",
        "name": "Premium 1",
        "features": [
            {
                "value": True,
                "text": "Backup channels and roles"
            }
        ],
        "button": '<a class="btn btn-outline-secondary my-sm-0" href="/patreon"><span class="align-middle">Buy</span></a>'
    },
    {
        "img": "/static/img/premium.jpg",
        "name": "Premium 2",
        "features": [
            {
                "value": True,
                "text": "Backup channels and roles"
            }
        ],
        "button": '<a class="btn btn-outline-secondary my-sm-0" href="/patreon"><span class="align-middle">Buy</span></a>'
    },
    {
        "img": "/static/img/premium.jpg",
        "name": "Premium 3",
        "features": [
            {
                "value": True,
                "text": "Backup channels and roles"
            }
        ],
        "button": '<a class="btn btn-outline-secondary my-sm-0" href="/patreon"><span class="align-middle">Buy</span></a>'
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
