# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django_comments_xtd.models import XtdComment
from django.contrib import comments
from django.core.urlresolvers import reverse
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
        'object_list': Category.objects.filter(taxonomy=taxonomy)
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


class MenuItem(object):
    html_id = None

    def __init__(self, title, url, html_id=None):
        self.title = title
        self.url = url
        self.html_id = html_id

    def check_active(self, chooser, value):
        self.active = chooser == 'url' and value == self.url


class ModelMenuItem(object):
    def __init__(self, obj, title=None, html_id=None):
        self.obj = obj
        self.title = title or unicode(obj)
        self.url = obj.get_absolute_url()
        self.html_id = html_id

    def check_active(self, chooser, value):
        self.active = (chooser == 'object' and value == self.obj or
                        chooser == 'objects' and self.obj in value)

class CategoryMenuItem(ModelMenuItem):
    def check_active(self, chooser, value):
        super(CategoryMenuItem, self).check_active(chooser, value)
        self.active = (self.active or
                       (chooser == 'object' and isinstance(value, Entry) and
                        self.obj in value.categories.all()))


class EntryTypeMenuItem(object):
    def __init__(self, title, type_, html_id=None):
        self.type = type_
        self.title = title
        self.url = reverse('migdal_entry_list_%s' % type_)
        self.html_id = html_id

    def check_active(self, chooser, value):
        self.active = (chooser == 'object' and isinstance(value, Entry)
                        and value.type == self.type or
                        chooser == 'entry_type' and value == self.type)

@register.inclusion_tag('migdal/menu.html', takes_context=True)
def main_menu(context, chooser=None, value=None):
    items = [
        ModelMenuItem(Entry.objects.get(slug_pl='o-nas')),
        EntryTypeMenuItem(_(u'Publications'), u'publications'),
        MenuItem(_(u'Events'), reverse('events')),
        CategoryMenuItem(Category.objects.get(slug_pl='stanowisko'), title=_('Positions')),
        CategoryMenuItem(Category.objects.get(slug_pl='pierwsza-pomoc')),
    ]
    if context['request'].LANGUAGE_CODE == 'pl':
        items.append(MenuItem(u'en', '/en/', html_id='item-lang'))
    else:
        items.append(MenuItem(u'pl', '/', html_id='item-lang'))
    for item in items:
        item.check_active(chooser, value)
    return {'items': items}
