from django.template import Library

register = Library()


@register.inclusion_tag('fnpdjango/prevnext/previous.html', takes_context=True)
def previous_page(context, fallback=None, fallback_title=None):
    current = context['page_obj'].number
    if current > 1:
        return {'number': current - 1, 'title': None, 'url': None}
    else:
        return {'number': None, 'title': fallback_title, 'url': fallback}


@register.inclusion_tag('fnpdjango/prevnext/next.html', takes_context=True)
def next_page(context, fallback=None, fallback_title=None):
    current = context['page_obj'].number
    page_range = context['paginator'].page_range
    if current < page_range[-1]:
        return {'number': current + 1, 'title': None, 'url': None}
    else:
        return {'number': None, 'title': fallback_title, 'url': fallback}


@register.inclusion_tag('fnpdjango/prevnext/prevnext.html', takes_context=True)
def prevnext(context):
    return context
