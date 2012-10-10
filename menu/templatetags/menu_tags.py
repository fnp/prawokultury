from django import template
from fnpdjango.utils.views import get_current_object
from ..models import items

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def main_menu(context):
    request = context['request']
    obj = get_current_object(request)
    for item in items:
        item.check_active(request, obj)
    return {'items': items}
