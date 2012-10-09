# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from itertools import chain
from migdal.models import Entry
from migdal import app_settings
from django.utils.translation import get_language


def entry_list(entry_type=None, category=None, promobox=False):
    lang = get_language()
    object_list = Entry.objects.filter(**{"published_%s" % lang: True}
        ).order_by('-published_at_%s' % lang)
    if entry_type:
        object_list = object_list.filter(type=entry_type.db)
    else:
        object_list = object_list.filter(
            type__in=[t.db for t in app_settings.TYPES if t.on_main])
    if category:
        object_list = object_list.filter(categories=category)

    if promobox:
        promo = list(object_list.filter(promo=True)[:promobox])
        #object_list = object_list.exclude(pk__in=[p.pk for p in promo])
        object_list.promobox = promo

    return object_list
