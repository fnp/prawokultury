# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from textile import Textile


class TextilePL(Textile):
    glyph_defaults = [(name, repl) 
        for (name, repl) in Textile.glyph_defaults
        if name != 'txt_quote_double_open']
    glyph_defaults.append(('txt_quote_double_open', '&#8222;'))


def textile_pl(text):
    return TextilePL().textile(text)


def textile_restricted_pl(text):
    return TextilePL(restricted=True, lite=True,
                   noimage=True, auto_link=False).textile(
                        text, rel='nofollow')


class LazyUGettextLazy(object):
    """You can use it to internationalize strings in settings.

    Just import this class as gettext.
    """
    _ = lambda s: s
    real = False

    def __init__(self, text):
        self.text = text

    def __unicode__(self):
        if not self.real:
            from django.utils.translation import ugettext_lazy
            LazyUGettextLazy._ = staticmethod(ugettext_lazy)
            LazyUGettextLazy.real = True
        return unicode(self._(self.text))


class AppSettings(object):
    """Allows specyfying custom settings for an app, with default values.

    Just subclass, set some properties and instantiate with a prefix.
    Getting a SETTING from an instance will check for prefix_SETTING
    in project settings if set, else take the default. The value will be
    then filtered through _more_SETTING method, if there is one.

    """
    def __init__(self, prefix):
        self._prefix = prefix

    def __getattribute__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        value = getattr(settings,
                         "%s_%s" % (self._prefix, name),
                         object.__getattribute__(self, name))
        more = "_more_%s" % name
        if hasattr(self, more):
            value = getattr(self, more)(value)
        return value


def serve_file(url):
    if settings.X_ACCEL_REDIRECT:
        response = HttpResponse()
        response['Content-Type'] = ""
        response['X-Accel-Redirect'] = url
        return response
    else:
        return HttpResponseRedirect(url)
