# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.contrib import admin
from events.models import Event
from migdal.helpers import translated_fields


class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('date', 'link')}),
    ) + tuple(
        (ln, {'fields': (
            ('published_%s' % lc),
            'title_%s' % lc,
            'organizer_%s' % lc,
            'place_%s' % lc,
            )})
        for lc, ln in settings.LANGUAGES
    )
    list_display = translated_fields(
        ('title', 'place', 'organizer'), settings.LANGUAGES
        ) + ('date',)
    date_hierarchy = 'date'


admin.site.register(Event, EventAdmin)
