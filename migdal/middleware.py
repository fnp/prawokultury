# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.utils import translation
from django.conf import settings
from django.http import Http404


class URLLocaleMiddleware(object):
    """Decides which translation to use, based on path only."""

    def process_request(self, request):
        language = translation.get_language_from_path(request.path_info)
        if language == settings.LANGUAGE_CODE:
            raise Http404
        if language:
            translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()
        translation.deactivate()
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response
