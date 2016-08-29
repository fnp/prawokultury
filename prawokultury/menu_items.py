# -*- coding: utf-8
from migdal.models import Category, Entry
from menu.helpers import ObjectMenuItem, MenuItem, ModelMenuItem
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


ITEMS = [
    ObjectMenuItem(obj_get=lambda: Entry.published_objects.get(slug_pl='o-nas')),
    ModelMenuItem(Entry, reverse_lazy('migdal_entry_list_publications'),
                  field_lookups={'type': 'publications'}, title=_('Publications')),
    MenuItem(reverse_lazy('events'), _('Events'), langs=['en']),
    MenuItem('/kurs/', u'Kurs dla uczelni', langs=['pl']),
    ObjectMenuItem(
        obj_get=lambda: Category.objects.get(slug_pl='stanowisko'),
        rev_lookups={Entry: 'categories'},
        title=_('Positions')),
    MenuItem(
        reverse_lazy('questions'), _('First aid')),
    ObjectMenuItem(
        obj_get=lambda: Entry.published_objects.get(slug_pl='pierwsza-pomoc'),
        title=_('Guide')),
]
