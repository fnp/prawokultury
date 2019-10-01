# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.sitemaps.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import ugettext_lazy as _, string_concat
import django_cas_ng.views
from fnpdjango.utils.urls import i18n_patterns
from events.urls import urlpatterns as events_urlpatterns
from migdal.urls import urlpatterns as migdal_urlpatterns
from migdal.sitemap import sitemaps as migdal_sitemaps
from questions.sitemap import sitemaps as question_sitemaps


urlpatterns = [
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),

    url(r'^sitemap\.xml$', django.contrib.sitemaps.views.sitemap, {
        'sitemaps': dict(migdal_sitemaps.items() + question_sitemaps.items())
    }),

    url(r'^accounts/login/$', django_cas_ng.views.login),
    url(r'^accounts/logout/$', django_cas_ng.views.logout),
    url(r'^admin/login/$', django_cas_ng.views.login),
    url(r'^admin/logout/$', django_cas_ng.views.logout),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    url(string_concat(r'^', _('events'), r'/'), include('events.urls')),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^pierwsza-pomoc/', include('questions.urls')),
    url(string_concat(r'^', _('shop'), r'/'), include('shop.urls')),
) + migdal_urlpatterns 

if settings.DEBUG:
    import django.views.static
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
   ]

urlpatterns += staticfiles_urlpatterns()
