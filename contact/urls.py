from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<form_tag>[^/]+)/$', views.form, name='contact_form'),
    url(r'^(?P<form_tag>[^/]+)/thanks/$', views.thanks, name='contact_thanks'),
    url(r'^attachment/(?P<contact_id>\d+)/(?P<tag>[^/]+)/$',
            views.attachment, name='contact_attachment'),
    url(r'^(?P<form_tag>[^/]+)/(?P<key>[^/]{30})/$', views.form, name='contact_form_key'),
]
