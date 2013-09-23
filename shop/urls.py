# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf.urls import patterns, url, include
from django.utils.translation import ugettext_lazy as _

from .views import ThanksView, NoThanksView, OfferDetailView


urlpatterns = patterns('',
    url(r'^kup/(?P<slug>[^/]+)/$', OfferDetailView.as_view(), name='shop_buy'),
    url(r'^dziekujemy/$', ThanksView.as_view(), name='shop_thanks'),
    url(r'^niepowodzenie/$', NoThanksView.as_view(), name='shop_nothanks'),
    url(r'^getpaid/', include('getpaid.urls')),
)
