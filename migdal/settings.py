# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from migdal.helpers import EntryType


def app_setting(global_name, default):
    try:
        return getattr(settings, global_name)
    except AttributeError:
        return default

# Types of entries:
# (slug, commentable, on main)
TYPES = app_setting('MIGDAL_TYPES', (
            EntryType('news', _('news'), commentable=True, on_main=True),
            EntryType('publications', _('publications'), commentable=False, on_main=False),
            EntryType('info', _('info'), commentable=False, on_main=False),
        ))
TYPES_DICT = dict((t.db, t) for t in TYPES)
TYPES_ON_MAIN = tuple(t.db for t in TYPES if t.on_main)
# FIXME: if only news is on_main, `news/` should either throw 404 or redirect to main

LANGUAGES = app_setting('MIGDAL_LANGUAGES', settings.LANGUAGES)
LANGUAGE_CODE = app_setting('MIGDAL_LANGUAGE_CODE', settings.LANGUAGE_CODE)
OBLIGATORY_LANGUAGES = app_setting('MIGDAL_OBLIGATORY', tuple(
    lang for lang in LANGUAGES if lang[0]==LANGUAGE_CODE))
OPTIONAL_LANGUAGES = tuple(lang for lang in LANGUAGES if lang not in OBLIGATORY_LANGUAGES)
