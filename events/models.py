# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from fnpdjango.utils.models.translation import add_translatable


class Event(models.Model):
    date = models.DateTimeField(_('date'), max_length=255, db_index=True)
    date_end = models.DateTimeField(_('end date'), max_length=255, 
        db_index=True, blank=True)
    link = models.URLField(_('link'))

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['date']

    def __unicode__(self):
        return self.title

    def clean(self):
        if self.date_end:
            if self.date_end < self.date:
                raise ValidationError(
                    ugettext("End date must not be earlier than start."))
        else:
            self.date_end = self.date
        for lc, ln in settings.LANGUAGES:
            if (getattr(self, "published_%s" % lc) and
                    not getattr(self, "title_%s" % lc)):
                raise ValidationError(
                    ugettext("Published event should have a title in relevant language (%s).") % lc)


add_translatable(Event, {
    'title': models.CharField(_('title'), max_length=255, blank=True),
    'organizer': models.CharField(_('organizer'), max_length=255,
            db_index=True, blank=True),
    'place': models.CharField(_('place'), max_length=255, blank=True),
    'published': models.BooleanField(_('published'), default=False),
})
