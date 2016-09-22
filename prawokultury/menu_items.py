# -*- coding: utf-8 -*-
from migdal.models import Entry
from menu.helpers import ObjectMenuItem

ITEMS = []


def add_entry(**qs):
    try:
        entry = Entry.objects.get(**qs)
    except Entry.DoesNotExist:
        return
    if not entry.published:
        return
    ITEMS.append(ObjectMenuItem(entry))

add_entry(slug_pl='co')
add_entry(slug_pl='gdzie')
add_entry(pk=25)
add_entry(slug_pl='program')
# add_entry(slug_pl='faq')
add_entry(slug_pl='wyszehrad')
# add_entry(slug_pl='wez-udzial')
add_entry(slug_pl='materialy')
# add_entry(pk=25)
# add_entry(slug_pl='warsztaty')
add_entry(slug_pl='poprzednie')
add_entry(slug_pl='kontakt')
add_entry(slug_pl='faq')
