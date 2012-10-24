from django.conf import settings
from django.core.urlresolvers import resolve, reverse, Resolver404
from django import template
from django.utils import translation
from ..utils.views import get_current_object

register = template.Library()


@register.inclusion_tag('fnpdjango/lang_switcher.html', takes_context=True)
def lang_switcher(context):
    """Context-aware language switcher.

    Use ..utils.views.set_current_object to provide the context.
    """
    request = context['request']
    obj = get_current_object(request)
    languages = settings.LANGUAGES
    if hasattr(obj, 'get_available_languages'):
        available_languages = set(obj.get_available_languages())
        languages = [lang for lang in languages if lang[0] in available_languages]
    return {
        'request': request,
        'languages': languages,
    }


@register.filter
def get_here_url(request, lang):
    obj = get_current_object(request, for_url=True)
    if hasattr(obj, 'get_absolute_url'):
        with translation.override(lang):
            url = obj.get_absolute_url()
    else:
        try:
            match = resolve(request.get_full_path())
        except Resolver404:
            match = resolve('/')
        view = match.url_name
        if view is None:
            view = match.func
        if lang is None:
            lang = translation.get_language()
        with translation.override(lang):
            url = reverse(view, args=match.args, kwargs=match.kwargs)
    return url


