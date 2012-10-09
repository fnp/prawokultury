from django import template
from django.utils.safestring import mark_safe
from ..utils.text import textilepl

register = template.Library()


@register.filter
def textile_pl(node):
    return mark_safe(textile.textile_pl(node))

@register.filter
def textile_restricted_pl(node):
    return mark_safe(textile.textile_restricted_pl(node))
