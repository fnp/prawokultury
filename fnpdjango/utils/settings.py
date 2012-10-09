"""
Utilities for global settings.
"""


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


