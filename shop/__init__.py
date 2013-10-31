# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings as settings
from fnpdjango.utils.app import AppSettings


class Settings(AppSettings):
    """Default settings for funding app."""
    DEFAULT_LANGUAGE = u'pl'


app_settings = Settings('SHOP')
