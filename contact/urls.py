from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('contact.views',
    url(r'^(?P<form_tag>[^/]+)/$', views.form, name='contact_form'),
    url(r'^(?P<form_tag>[^/]+)/thanks/$', views.thanks, name='contact_thanks'),
    url(r'^attachment/(?P<contact_id>\d+)/(?P<tag>[^/]+)/$',
            views.attachment, name='contact_attachment'),
)
