# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
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



class LazyUGettextLazy():
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
