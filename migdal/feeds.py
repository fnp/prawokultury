# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _, string_concat
from migdal import api
from migdal.models import Category
from migdal.settings import TYPES_DICT


class EntriesFeed(Feed):
    def get_object(self, request, type_db=None, category_slug=None):
        lang = request.LANGUAGE_CODE
        if category_slug:
            category = get_object_or_404(Category, **{'slug_%s' % lang: category_slug})
        else:
            category = None
        if type_db:
            entry_type = TYPES_DICT[type_db]
        else:
            entry_type = None
        return {'entry_type': entry_type, 'category': category}

    def title(self, obj):
        t = "Prawo kultury, " + _("latest") + " "
        if obj['entry_type']:
            t += unicode(obj['entry_type'].slug)
        else:
            t += _("entries")
        if obj['category']:
            t += " " + _("in category") + " " + obj['category'].title
        return t

    def link(self, obj):
        if obj['category']:
            return reverse('migdal_category', args=[obj['category'].slug])
        if obj['entry_type']:
            return reverse('migdal_entry_list_%s' % obj['entry_type'].db)
        return reverse('migdal_main')

    def items(self, obj):
        return api.entry_list(**obj)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.lead
        image = item.image.url if item.image else "/static/img/square-logo.png"
        return string_concat("<img src='%s'/>" % image, item.lead)

    def item_pubdate(self, item):
        return item.date
