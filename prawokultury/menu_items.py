# -*- coding: utf-8
from migdal.models import Category, Entry
from menu.helpers import ObjectMenuItem, MenuItem, ModelMenuItem
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


ITEMS = []

ITEMS.append(ObjectMenuItem(
    obj_get=lambda:Entry.published_objects.get(slug_pl='o-nas')
))

ITEMS.append(ModelMenuItem(Entry, reverse_lazy('migdal_entry_list_publications'),
        field_lookups={'type': 'publications'}, title=_('Publications')))

ITEMS.append(MenuItem(reverse_lazy('events'), _('Events'),
        more_urls=(reverse_lazy('events_past'),)))

ITEMS.append(ObjectMenuItem(
    obj_get=lambda:Category.objects.get(slug_pl='stanowisko'),
    rev_lookups={Entry: 'categories'},
    title=_('Positions')
))

ITEMS.append(ObjectMenuItem(
    obj_get=lambda:Entry.published_objects.get(slug_pl='pierwsza-pomoc'),
    title=_('First aid in copyright')
))
