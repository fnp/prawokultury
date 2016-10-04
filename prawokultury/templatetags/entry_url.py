# -*- coding: utf-8 -*-
from django.template import Library
from migdal.models import Entry

register = Library()


@register.simple_tag()
def entry_url(slug_pl):
    return Entry.objects.get(slug_pl=slug_pl).get_absolute_url()