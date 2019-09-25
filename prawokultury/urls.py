# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import ugettext_lazy as _, string_concat
import django_cas.views
from fnpdjango.utils.urls import i18n_patterns
from migdal.urls import urlpatterns as migdal_urlpatterns


urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', django_cas.views.login),
    url(r'^accounts/logout/$', django_cas.views.logout),
] + i18n_patterns(
    url(r'^contact/', include('contact.urls')),
) + migdal_urlpatterns 

if settings.DEBUG:
    import django.views.static
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
   ]

urlpatterns += staticfiles_urlpatterns()
