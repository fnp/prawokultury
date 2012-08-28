# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from migdal.helpers import i18n_patterns
from migdal.urls import urlpatterns as migdal_urlpatterns
from django.utils.translation import ugettext_lazy as _, string_concat
from events.urls import urlpatterns as events_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
) + i18n_patterns('',
    url(string_concat(r'^', _('events'), r'/'), include('events.urls')),
    url(r'^comments/', include('django_comments_xtd.urls')),
) + migdal_urlpatterns 

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

urlpatterns += staticfiles_urlpatterns()
