# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django_comments_xtd.models import XtdComment
from django import template
from migdal.models import Category

register = template.Library()


@register.simple_tag
def entry_begin(entry):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_begin.html' % entry.type,
        'migdal/entry/entry_begin.html',
    ))
    context = {'object': entry}
    return t.render(template.Context(context))


@register.simple_tag
def entry_short(entry):
    t = template.loader.select_template((
        'migdal/entry/%s/entry_short.html' % entry.type,
        'migdal/entry/entry_short.html',
    ))
    context = {'object': entry}
    return t.render(template.Context(context))


@register.inclusion_tag('migdal/categories.html', takes_context=True)
def categories(context):
    context.update({'object_list': Category.objects.all()})
    return context


@register.inclusion_tag('migdal/last_comments.html')
def last_comments(limit=10):
    return {'object_list': 
        XtdComment.objects.filter(is_public=True, is_removed=False).order_by('-submit_date')[:limit]}
