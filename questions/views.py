# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import FormView
from .forms import QuestionForm
from .models import Question, Tag, TagCategory


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
                self.tag = Tag.objects.filter(items__question__published=True, slug=request.GET['tag'])[0]
            except IndexError:
                pass
        return super(QuestionListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Question.objects.filter(published=True
                ).order_by('-published_at')
        if self.tag:
            qs = qs.filter(tags=self.tag)
            self.tag.click_count += 1
            self.tag.save()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionListView, self).get_context_data(*args, **kwargs)
        context['tags'] = Tag.objects.filter(items__question__published=True
            ).annotate(c=models.Count('items__tag')).order_by('-c', 'slug')
        context['tag'] = self.tag
        context['tag_categories'] = TagCategory.objects.all().annotate(click_count = models.Sum('tags__click_count'))
        return context
