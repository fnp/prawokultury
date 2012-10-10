# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django_comments_xtd.models import XtdComment
from django.contrib import comments
from django import template
from migdal import app_settings
from migdal.models import Category, Entry
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.simple_tag(takes_context=True)
def entry_begin(context, entry, detail=False):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_begin.html' % entry.type,
        'migdal/entry/entry_begin.html',
    ))
    context = {
        'request': context['request'],
        'object': entry,
        'detail': detail,
    }
    return t.render(template.Context(context))


@register.simple_tag(takes_context=True)
def entry_short(context, entry):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_short.html' % entry.type,
        'migdal/entry/entry_short.html',
    ))
    context = {
        'request': context['request'],
        'object': entry,
    }
    return t.render(template.Context(context))


@register.simple_tag(takes_context=True)
def entry_promobox(context, entry, counter):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_promobox.html' % entry.type,
        'migdal/entry/entry_promobox.html',
    ))
    context = {
        'request': context['request'],
        'object': entry,
        'counter': counter,
    }
    return t.render(template.Context(context))


@register.inclusion_tag('migdal/categories.html', takes_context=True)
def categories(context, taxonomy):
    context = {
        'request': context['request'],
        'object_list': Category.objects.filter(taxonomy=taxonomy
                ).exclude(entry__isnull=True)
    }
    return context


@register.inclusion_tag('migdal/last_comments.html')
def last_comments(limit=app_settings.LAST_COMMENTS):
    return {'object_list': 
        XtdComment.objects.filter(is_public=True, is_removed=False).order_by('-submit_date')[:limit]}


@register.inclusion_tag(['comments/form.html'])
def entry_comment_form(entry):
    return {
            'form': comments.get_form()(entry),
            'next': entry.get_absolute_url(),
        }
