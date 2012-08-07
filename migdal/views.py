# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.shortcuts import get_object_or_404, render
from migdal import api
from migdal.models import Category, Entry
from migdal.settings import TYPES_DICT


def entry_list(request, type_db=None, category_slug=None):
    lang = request.LANGUAGE_CODE
    templates = ["migdal/entry/entry_list.html"]

    if category_slug:
        category = get_object_or_404(Category, **{'slug_%s' % lang: category_slug})
    else:
        category = None
    if type_db:
        entry_type = TYPES_DICT[type_db]
        # TODO: if it's the only on main, redirect to main
        templates = ["migdal/entry/%s/entry_list.html" % type_db] + templates
    else:
        entry_type = None

    object_list = api.entry_list(entry_type=entry_type, category=category)

    return render(request, templates, {
            'object_list': object_list,
            'category': category,
            'entry_type': entry_type,
        })


def entry(request, type_db, slug):
    lang = request.LANGUAGE_CODE
    args = {'type': type_db, 'slug_%s' % lang: slug, 'published_%s' % lang: True}
    # TODO: preview for admins
    entry = get_object_or_404(Entry, **args)

    templates = ["migdal/entry/entry_detail.html"]
    if type_db is not None:
        templates = ["migdal/entry/%s/entry_detail.html" % type_db] + templates
    return render(request, templates, {'entry': entry})
