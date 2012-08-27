# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf.urls import patterns, include, url
from django.utils.translation import string_concat, ugettext_lazy as _


urlpatterns = patterns('events.views',
    url(r'^$', 'events', name='events'),
    url(string_concat('^', _('past'), '/$'), 'events_past', name='events_past'),
)
