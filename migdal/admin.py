# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from migdal.models import Category, Entry, Attachment
from migdal import settings


def translated_fields(field_names, languages=settings.LANGUAGES):
    return tuple("%s_%s" % (field_name, lang_code)
                for field_name in field_names
                for lang_code, lang_name in languages
                )


class AttachmentInline(admin.TabularInline):
    model = Attachment
    readonly_fields = ['url']


class EntryAdmin(admin.ModelAdmin):
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
        for lc, ln in settings.OBLIGATORY_LANGUAGES
    ) + tuple(
        (ln, {'fields': (
            ('needed_%s' % lc, 'published_%s' % lc),
            'title_%s' % lc,
            'slug_%s' % lc,
            'lead_%s' % lc,
            'body_%s' % lc,
            )})
        for lc, ln in settings.OPTIONAL_LANGUAGES
    ) + (
        (_('Categories'), {'fields': ('categories',)}),
    )
    prepopulated_fields = dict([
            ("slug_%s" % lang_code, ("title_%s" % lang_code,))
            for lang_code, lang_name in settings.LANGUAGES
        ]) 

    list_display = translated_fields(('title',), settings.OBLIGATORY_LANGUAGES
            ) + ('type', 'date', 'author'
            ) + translated_fields(('published',)
            ) + translated_fields(('needed',), settings.OPTIONAL_LANGUAGES)
    list_filter = ('type',) + translated_fields(('published',)
            ) + translated_fields(('needed',), settings.OPTIONAL_LANGUAGES)
    inlines = (AttachmentInline,)


class CategoryAdmin(admin.ModelAdmin):
    list_display = translated_fields(('title', 'slug')) + ('taxonomy',)
    prepopulated_fields = dict([
            ("slug_%s" % lang_code, ("title_%s" % lang_code,))
            for lang_code, lang_name in settings.LANGUAGES
        ]) 


admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
