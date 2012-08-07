# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from events.models import Event


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Event), name='events'),
    #url(r'^(?P<slug>[^/]+)/$', DetailView.as_view(model=Event), name='news'),
)
