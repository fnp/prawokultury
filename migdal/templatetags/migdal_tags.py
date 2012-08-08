# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django_comments_xtd.models import XtdComment
from django.contrib import comments
from django import template
from migdal.models import Category

register = template.Library()


@register.simple_tag(takes_context=True)
def entry_begin(context, entry):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_begin.html' % entry.type,
        'migdal/entry/entry_begin.html',
    ))
    context.update({'object': entry})
    return t.render(template.Context(context))


@register.simple_tag(takes_context=True)
def entry_short(context, entry):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_short.html' % entry.type,
        'migdal/entry/entry_short.html',
    ))
    context.update({'object': entry})
    return t.render(template.Context(context))


@register.inclusion_tag('migdal/categories.html', takes_context=True)
def categories(context):
    context.update({'object_list': Category.objects.all()})
    return context


@register.inclusion_tag('migdal/last_comments.html')
def last_comments(limit=10):
    return {'object_list': 
        XtdComment.objects.filter(is_public=True, is_removed=False).order_by('-submit_date')[:limit]}


@register.inclusion_tag(['comments/form.html'])
def entry_comment_form(entry):
    return {
            'form': comments.get_form()(entry),
            'next': entry.get_absolute_url(),
        }