# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import ugettext_lazy as _, string_concat
from fnpdjango.utils.urls import i18n_patterns
from events.urls import urlpatterns as events_urlpatterns
from migdal.urls import urlpatterns as migdal_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

if 'django.contrib.sitemaps' in settings.INSTALLED_APPS:
    from migdal.sitemap import sitemaps as migdal_sitemaps
    from questions.sitemap import sitemaps as question_sitemaps
    sitemaps = dict(migdal_sitemaps.items() + question_sitemaps.items())
    urlpatterns += patterns('',
        url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {
            'sitemaps': sitemaps
        }),
    )

if 'django_cas' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^accounts/login/$', 'django_cas.views.login'),
        (r'^accounts/logout/$', 'django_cas.views.logout'),
    )

urlpatterns += i18n_patterns('',
    url(string_concat(r'^', _('events'), r'/'), include('events.urls')),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^prawnik/', include('questions.urls')),
) + migdal_urlpatterns 

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

urlpatterns += staticfiles_urlpatterns()
