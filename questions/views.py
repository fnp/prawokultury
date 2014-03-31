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
                tag = Tag.objects.get(slug=request.GET['tag'])
                assert Question.objects.filter(tags=self.tag).exists()
            except (Tag.DoesNotExist, AssertionError):
                pass
            else:
                self.tag = tag
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
        def get_cloud_size(clicks, relate_to):
            return '%.2f' % (0.7 + (float(clicks) / relate_to if relate_to != 0 else 0))
        
        context = super(QuestionListView, self).get_context_data(*args, **kwargs)
        context['tag'] = self.tag
        context['tag_categories'] = TagCategory.objects.all().annotate(click_count = models.Sum('tags__click_count'))
        context['tag_lists'] = dict()
        
        annotated_categories = dict()
        all_tags_click_count = Tag.objects.all().aggregate(models.Sum('click_count'))['click_count__sum']
        for category in context['tag_categories']:
            annotated_categories[category.id] = category
            category.cloud_size =  get_cloud_size(category.click_count, all_tags_click_count)

        # This wouldn't happen if we were using taggit without generic relations.
        tags = Tag.objects.raw("""
            SELECT t.category_id, t.click_count, t.id, t.name, t.slug, count(t.id) AS c
            FROM questions_tag t
            LEFT JOIN questions_tagcategory c ON c.id=t.category_id
            LEFT JOIN questions_tagitem i ON i.tag_id=t.id
            LEFT JOIN questions_question q ON q.id=i.object_id
            WHERE q.published
            GROUP BY t.category_id, t.click_count, t.id, t.name, t.slug, c.slug
            ORDER BY c.slug, c DESC, t.slug
            """)
        uncategorized_tags_click_count = Tag.objects.filter(category=None).aggregate(models.Sum('click_count'))['click_count__sum']
        for tag in tags:
            if tag.category:
                category_click_count = annotated_categories[tag.category.id].click_count
            else:
                category_click_count = uncategorized_tags_click_count
            tag.cloud_size = get_cloud_size(tag.click_count, category_click_count)
            context['tag_lists'].setdefault(tag.category.id if tag.category else 0, []).append(tag)
        context['has_uncategorized_tags'] = 0 in context['tag_lists']

        return context
