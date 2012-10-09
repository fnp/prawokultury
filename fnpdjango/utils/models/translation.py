"""
Utilities for creating multilingual fields in your apps.
"""

from copy import copy
from django.conf import settings
from django.utils.translation import get_language, string_concat


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


def add_translatable_index(index_class, fields, languages=None):
    """Adds some translatable fields to a search index."""
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
    """Generate a tuple of field names in translated versions."""
    return tuple("%s_%s" % (field_name, lang_code)
                for field_name in field_names
                for lang_code, lang_name in languages
                )
