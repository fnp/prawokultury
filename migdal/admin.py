# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from migdal.models import Category, Entry, Attachment
from migdal import app_settings
from migdal.helpers import translated_fields


class AttachmentInline(admin.TabularInline):
    model = Attachment
    readonly_fields = ['url']


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    fieldsets = (
        (None, {'fields': (('type', 'promo'), 'author', 'author_email', 'image')}),
    ) + tuple(
        (ln, {'fields': (
            ('published_%s' % lc),
            'title_%s' % lc,
            'slug_%s' % lc,
            'lead_%s' % lc,
            'body_%s' % lc,
            )})
        for lc, ln in app_settings.OBLIGATORY_LANGUAGES
    ) + tuple(
        (ln, {'fields': (
            ('needed_%s' % lc, 'published_%s' % lc),
            'title_%s' % lc,
            'slug_%s' % lc,
            'lead_%s' % lc,
            'body_%s' % lc,
            )})
        for lc, ln in app_settings.OPTIONAL_LANGUAGES
    ) + (
        (_('Categories'), {'fields': ('categories',)}),
    )
    prepopulated_fields = dict([
            ("slug_%s" % lang_code, ("title_%s" % lang_code,))
            for lang_code, lang_name in settings.LANGUAGES
        ]) 

    list_display = translated_fields(('title',), app_settings.OBLIGATORY_LANGUAGES
            ) + ('type', 'date', 'author', 'promo'
            ) + translated_fields(('published',)
            ) + translated_fields(('needed',), app_settings.OPTIONAL_LANGUAGES)
    list_filter = ('type', 'promo') + translated_fields(('published',)
            ) + translated_fields(('needed',), app_settings.OPTIONAL_LANGUAGES)
    inlines = (AttachmentInline,)


class CategoryAdmin(admin.ModelAdmin):
    list_display = translated_fields(('title', 'slug')) + ('taxonomy',)
    prepopulated_fields = dict([
            ("slug_%s" % lang_code, ("title_%s" % lang_code,))
            for lang_code, lang_name in settings.LANGUAGES
        ]) 


admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
