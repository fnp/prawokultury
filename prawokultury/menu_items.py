# -*- coding: utf-8 -*-
from menu.helpers import ObjectMenuItem

ITEMS = []


def add_entry(**qs):
    ITEMS.append(ObjectMenuItem(qs))


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
