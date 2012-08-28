# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.contrib import admin
from events.models import Event
from migdal.helpers import translated_fields


class EventAdmin(admin.ModelAdmin):
    list_display = translated_fields(
        ('title', 'place', 'organizer'), settings.LANGUAGES
        ) + ('date',)
    date_hierarchy = 'date'


admin.site.register(Event, EventAdmin)
