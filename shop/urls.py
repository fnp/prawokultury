# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf.urls import url, include
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from getpaid.backends.payu.views import OnlineView
from prawokultury.middleware import honeypot_exempt
from .views import ThanksView, NoThanksView, OfferDetailView


urlpatterns = [
    url(r'^kup/(?P<slug>[^/]+)/$', OfferDetailView.as_view(), name='shop_buy'),
    url(r'^dziekujemy/(?P<pk>\d+)/$', ThanksView.as_view(), name='shop_thanks'),
    url(r'^niepowodzenie/(?P<pk>\d+)/$', NoThanksView.as_view(), name='shop_nothanks'),
    url(r'^getpaid/getpaid.backends.payu/online/$', 
            honeypot_exempt(csrf_exempt(OnlineView.as_view())),
            name='getpaid-payu-online'),
    url(r'^getpaid/', include('getpaid.urls')),
]
