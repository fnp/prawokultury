# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.db import models
from django.utils.translation import ugettext_lazy as _
from migdal.helpers import add_translatable


class Event(models.Model):
    date = models.DateTimeField(_('date'), max_length=255, db_index=True)
    link = models.URLField(_('link'))

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['date']

    def __unicode__(self):
        return self.title


add_translatable(Event, {
    'title': models.CharField(_('title'), max_length=255),
    'organizer': models.CharField(_('organizer'), max_length=255, db_index=True),
    'place': models.CharField(_('place'), max_length=255),
})
