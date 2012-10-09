"""
Utilities for urlconfs.
"""

import re
from django.conf import settings
from django.conf.urls import patterns
from django.core.urlresolvers import LocaleRegexURLResolver
from django.utils.translation import get_language, string_concat


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
