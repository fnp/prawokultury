# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django import template
from django.utils.safestring import mark_safe
from prawokultury import helpers

register = template.Library()


@register.filter
def textile_pl(node):
    return mark_safe(helpers.textile_pl(node))

@register.filter
def textile_restricted_pl(node):
    return mark_safe(helpers.textile_restricted_pl(node))
