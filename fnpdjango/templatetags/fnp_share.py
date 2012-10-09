from django.template import Library

register = Library()


@register.inclusion_tag('fnpdjango/share.html', takes_context=True)
def share(context, url, description, iconset=""):
    return {
        'url': url,
        'description': description,
        'iconset': iconset,
        'request': context['request'],
    }
