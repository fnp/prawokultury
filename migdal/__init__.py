# -*- coding: utf-8 -*-
"""
Migdal (מִגְדָּל) is a multilingual blog Django app.

Author: Radek Czajka <radoslaw.czajka@nowoczesnapolska.org.pl>
"""
from django.conf import settings
from prawokultury.helpers import AppSettings
from django.utils.translation import ugettext_lazy as _
from migdal.helpers import EntryType


class Settings(AppSettings):
    # Types of entries:
    # (slug, commentable, on main)
    TYPES = (
            EntryType('news', _('news'), commentable=True, on_main=True),
            EntryType('publications', _('publications'), commentable=False, on_main=False),
            EntryType('info', _('info'), commentable=False, on_main=False),
        )
    TYPE_SUBMIT = 'news'
    TAXONOMIES = (
        ('topics', _('topics')),
        ('types', _('types')),
    )
    LAST_COMMENTS = 5

    TYPES_DICT = None
    def _more_TYPES_DICT(self, value):
        return dict((t.db, t) for t in self.TYPES)

    TYPES_ON_MAIN = None
    def _more_TYPES_ON_MAIN(self, value):
        return tuple(t.db for t in self.TYPES if t.on_main)

    OBLIGATORY_LANGUAGES = None
    def _more_OBLIGATORY_LANGUAGES(self, value):
        return value or tuple(lang for lang in settings.LANGUAGES
                        if lang[0] == settings.LANGUAGE_CODE)

    OPTIONAL_LANGUAGES = None
    def _more_OPTIONAL_LANGUAGES(self, value):
        return tuple(lang for lang in settings.LANGUAGES
                        if lang not in self.OBLIGATORY_LANGUAGES)

app_settings = Settings('MIGDAL')



