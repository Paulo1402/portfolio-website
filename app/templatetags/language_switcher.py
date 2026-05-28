from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def switch_language_url(context, language_code):
    request = context.get("request")
    if request is None:
        return f"/{language_code}/"

    path = request.path or "/"
    for code, _ in settings.LANGUAGES:
        prefix = f"/{code}/"
        if path.startswith(prefix):
            return f"/{language_code}/" + path[len(prefix) :]

    if not path.startswith("/"):
        path = f"/{path}"
    return f"/{language_code}{path}"
