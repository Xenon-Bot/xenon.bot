from sanic import response


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
