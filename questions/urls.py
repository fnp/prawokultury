# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from .models import Question
from .views import QuestionFormView

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=Question.objects.filter(published=True
            ).order_by('-published_at')),
        name="questions"
    ),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(model=Question),
        name="questions_question"),
    url(r'^pytanie/$',
        QuestionFormView.as_view(),
        name="questions_form",
    ),
    url(r'^pytanie/dziekujemy/$',
        TemplateView.as_view(
            template_name="questions/question_thanks.html",
        ),
        name="questions_thanks"
    ),
)
