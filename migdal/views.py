# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.shortcuts import get_object_or_404, render, redirect
from migdal import api
from migdal.forms import get_submit_form
from migdal.models import Category, Entry
from migdal.settings import TYPES_DICT, TYPES_ON_MAIN, TYPE_SUBMIT


def entry_list(request, type_db=None, category_slug=None):
    lang = request.LANGUAGE_CODE
    templates = ["migdal/entry/entry_list.html"]

    if type_db:
        if TYPES_ON_MAIN == (type_db,):
            return redirect('migdal_main')
        entry_type = TYPES_DICT[type_db]
        templates = ["migdal/entry/%s/entry_list.html" % type_db] + templates
        submit = type_db == TYPE_SUBMIT
    else:
        submit = TYPES_ON_MAIN == (TYPE_SUBMIT,)
        entry_type = None

    if category_slug:
        category = get_object_or_404(Category, **{'slug_%s' % lang: category_slug})
    else:
        category = None

    object_list = api.entry_list(entry_type=entry_type, category=category)

    return render(request, templates, {
            'object_list': object_list,
            'category': category,
            'entry_type': entry_type,
            'submit': submit,
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


def submit(request):
    if request.method == 'POST':
        submit_form = get_submit_form(request.POST)
        if submit_form.is_valid():
            submit_form.save()
            return redirect('migdal_submit_thanks')
    else:
        submit_form = get_submit_form()

    return render(request, 'migdal/entry/submit.html', {
            'submit_form': submit_form,
        })

def submit_thanks(request):
    return render(request, "migdal/entry/submit_thanks.html")