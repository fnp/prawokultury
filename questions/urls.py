# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf.urls import url
from django.views.generic import DetailView, TemplateView
from .models import Question
from .views import QuestionFormView, QuestionListView

urlpatterns = [
    url(r'^$',
        QuestionListView.as_view(),
        name="questions"
    ),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(queryset=Question.objects.filter(published=True)),
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
]
