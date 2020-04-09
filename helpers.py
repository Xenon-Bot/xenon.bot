from sanic import response
import jwt
import json


def template(template_name):
    def predicate(handler):
        async def wrapper(request, *args, **kwargs):
            context = await handler(request, *args, **kwargs)
            if context is None:
                context = {}

            template = request.app.jinja2.get_template(template_name)
            rendered = await template.render_async(context)
            return response.html(rendered)

        return wrapper

    return predicate


def requires_body(*fields):
    def predicate(handler):
        async def wrapper(request, *args, **kwargs):
            data = request.json
            if data is None:
                return response.json({"error": "JSON body required"}, status=400)

            for field in fields:
                if field not in data.keys():
                    return response.json({"error": f"Field '{field}' is required"}, status=400)

            return await handler(request, *args, **kwargs)

        return wrapper

    return predicate


def encode_jwt(app, data):
    return jwt.encode(data, app.config.JWT_SECRET, algorithm='HS256')


def decode_jwt(app, token):
    return jwt.decode(token, app.config.JWT_SECRET, algorithms=['HS256'])


async def json_or_text(http_resp):
    text = await http_resp.text(encoding='utf-8')
    try:
        if http_resp.headers['content-type'] == 'application/json':
            return json.loads(text)
    except KeyError:
        # Thanks Cloudflare
        pass

    return text
