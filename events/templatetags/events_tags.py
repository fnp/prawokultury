# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django import template
from events import app_settings
from events.models import Event

register = template.Library()
from datetime import datetime


@register.inclusion_tag('events/snippets/events_box.html', takes_context=True)
def events_box(context, limit=app_settings.BOX_LENGTH):
    objects = Event.objects.filter(date__gte=datetime.now())[:limit]
    return {'objects': objects}
