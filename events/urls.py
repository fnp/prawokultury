# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf.urls import include, url
from django.utils.translation import string_concat, ugettext_lazy as _
from . import views


urlpatterns = [
    url(r'^$', views.events, name='events'),
    url(string_concat('^', _('past'), '/$'), views.events_past, name='events_past'),
]
