# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .forms import QuestionForm
from .models import Question, Tag


class QuestionFormView(FormView):
    form_class = QuestionForm
    template_name = "questions/question_form.html"
    success_url = reverse_lazy("questions_thanks")

    def form_valid(self, form):
        form.save()
        return super(QuestionFormView, self).form_valid(form)


class QuestionListView(ListView):
    def get(self, request, *args, **kwargs):
        self.tag = None
        if 'tag' in request.GET:
            try:
                self.tag = Tag.objects.get(slug=request.GET['tag'])
            except Tag.DoesNotExist:
                pass
        return super(QuestionListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Question.objects.filter(published=True
                ).order_by('-published_at')
        if 'tag' in self.request.GET:
            qs = qs.filter(tags__slug=self.request.GET['tag'])
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionListView, self).get_context_data(*args, **kwargs)
        context['tags'] = Tag.objects.all()
        context['tag'] = self.tag
        return context
