"""
Basic utilities for applications.
"""


from django.conf import settings


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
