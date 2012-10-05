# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from collections import namedtuple
from copy import copy
import re
from django.conf import settings
from django.conf.urls import patterns
from django.core.urlresolvers import LocaleRegexURLResolver
from django.utils.translation import get_language, string_concat


class EntryType(object):
    def __init__(self, db, slug, commentable=False, on_main=False,
            promotable=False, categorized=False):
        self.db = db
        self.slug = slug
        self.commentable = commentable
        self.on_main = on_main
        self.promotable = promotable
        self.categorized = categorized

    def __unicode__(self):
        return unicode(self.slug)


def field_getter(name):
    @property
    def getter(self):
        val = getattr(self, "%s_%s" % (name, get_language()), None)
        if not val:
            val = getattr(self, "%s_%s" % (name, settings.LANGUAGE_CODE))
        return val
    return getter


def add_translatable(model, fields, languages=None):
    """Adds some translatable fields to a model, and a getter."""
    if languages is None:
        languages = settings.LANGUAGES
    for name, field in fields.items():
        for lang_code, lang_name in languages:
            new_field = copy(field)
            if field.verbose_name:
                new_field.verbose_name = string_concat(field.verbose_name, ' [%s]' % lang_code)
            new_field.contribute_to_class(model, "%s_%s" % (name, lang_code))
        setattr(model, name, field_getter(name))
        # add setter?


class MyLocaleRegexURLResolver(LocaleRegexURLResolver):
    """
    A URL resolver that always matches the active language code as URL prefix.

    Rather than taking a regex argument, we just override the ``regex``
    function to always return the active language-code as regex.
    """
    @property
    def regex(self):
        language_code = get_language()
        if language_code == settings.LANGUAGE_CODE:
            return re.compile('')
        if language_code not in self._regex_dict:
            regex_compiled = re.compile('^%s/' % language_code, re.UNICODE)
            self._regex_dict[language_code] = regex_compiled
        return self._regex_dict[language_code]


def i18n_patterns(prefix, *args):
    """
    Adds the language code prefix to every URL pattern within this
    function. This may only be used in the root URLconf, not in an included
    URLconf.

    """
    pattern_list = patterns(prefix, *args)
    if not settings.USE_I18N:
        return pattern_list
    return pattern_list + [MyLocaleRegexURLResolver(pattern_list)]


def add_translatable_index(index_class, fields, languages=None):
    """Adds some translatable fields to a search index, and a getter."""
    if languages is None:
        languages = settings.LANGUAGES
    for name, field in fields.items():
        for lang_code, lang_name in languages:
            new_field = copy(field)
            fname = "%s_%s" % (name, lang_code)
            new_field.index_fieldname = new_field.index_fieldname \
                and "%s_%s" % (new_field.index_fieldname, lang_code) \
                or fname
            new_field.model_attr = new_field.model_attr \
                and "%s_%s" % (new_field.model_attr, lang_code) \
                or fname
            setattr(index_class, fname, new_field)
            index_class.fields[fname] = new_field


def translated_fields(field_names, languages=settings.LANGUAGES):
    return tuple("%s_%s" % (field_name, lang_code)
                for field_name in field_names
                for lang_code, lang_name in languages
                )
