# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from datetime import datetime
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.template import loader, Context
from django.utils.translation import get_language, ugettext_lazy as _, ugettext
from django_comments_xtd.models import XtdComment
from markupfield.fields import MarkupField
from migdal import app_settings
from fnpdjango.utils.models.translation import add_translatable
from migdal.fields import SlugNullField

class Category(models.Model):
    taxonomy = models.CharField(_('taxonomy'), max_length=32,
                    choices=app_settings.TAXONOMIES)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('migdal_category', [self.slug])


add_translatable(Category, {
    'title': models.CharField(max_length=64, unique=True, db_index=True),
    'slug': models.SlugField(unique=True, db_index=True),
})


class Entry(models.Model):
    type = models.CharField(max_length=16,
            choices=((t.db, t.slug) for t in app_settings.TYPES),
            db_index=True)
    date = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    changed_at = models.DateTimeField(_('changed at'), auto_now=True, db_index=True)
    author = models.CharField(_('author'), max_length=128)
    author_email = models.EmailField(_('author email'), max_length=128, null=True, blank=True,
            help_text=_('Used only to display gravatar and send notifications.'))
    image = models.ImageField(_('image'), upload_to='entry/image/', null=True, blank=True)
    promo = models.BooleanField(_('promoted'), default=False)
    categories = models.ManyToManyField(Category, null=True, blank=True, verbose_name=_('categories'))

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ['-date']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = type(self).objects.get(pk=self.pk)
            published_now = False
            for lc, ln in settings.LANGUAGES:
                if (getattr(self, "published_%s" % lc)
                        and getattr(self, "published_at_%s" % lc) is None):
                    setattr(self, "published_at_%s" % lc, datetime.now())
                    published_now = True
            if published_now:
                self.notify_author_published()
        super(Entry, self).save(*args, **kwargs)

    def clean(self):
        for lc, ln in settings.LANGUAGES:
            if (getattr(self, "published_%s" % lc) and
                    not getattr(self, "slug_%s" % lc)):
                raise ValidationError(
                    ugettext("Published entry should have a slug in relevant language (%s).") % lc)

    @models.permalink
    def get_absolute_url(self):
        return ('migdal_entry_%s' % self.type, [self.slug])

    def get_type(self):
        return dict(app_settings.TYPES_DICT)[self.type]

    def notify_author_published(self):
        if not self.author_email:
            return
        site = Site.objects.get_current()
        mail_text = loader.get_template('migdal/mail/published.txt').render(
            Context({
                'entry': self,
                'site': site,
            }))
        send_mail(
            ugettext(u'Your story has been published at %s.') % site.domain,
            mail_text, settings.SERVER_EMAIL, [self.author_email]
        )


add_translatable(Entry, languages=app_settings.OPTIONAL_LANGUAGES, fields={
    'needed': models.CharField(_('needed'), max_length=1, db_index=True, choices=(
                ('n', _('Unneeded')), ('w', _('Needed')), ('y', _('Done'))),
                default='n'),
})

add_translatable(Entry, {
    'slug': SlugNullField(unique=True, db_index=True, null=True, blank=True),
    'title': models.CharField(_('title'), max_length=255, null=True, blank=True),
    'lead': MarkupField(_('lead'), markup_type='textile_pl', null=True, blank=True,
                help_text=_('Use <a href="http://textile.thresholdstate.com/">Textile</a> syntax.')),
    'body': MarkupField(_('body'), markup_type='textile_pl', null=True, blank=True,
                help_text=_('Use <a href="http://textile.thresholdstate.com/">Textile</a> syntax.')),
    'published': models.BooleanField(_('published'), default=False),
    'published_at': models.DateTimeField(_('published at'), null=True, blank=True),
})


class Attachment(models.Model):
    file = models.FileField(_('file'), upload_to='entry/attach/')
    entry = models.ForeignKey(Entry)

    def url(self):
        return self.file.url if self.file else ''



def notify_new_comment(sender, instance, created, **kwargs):
    if (created and isinstance(instance.content_object, Entry) and
                instance.content_object.author_email):
        site = Site.objects.get_current()
        mail_text = loader.get_template('migdal/mail/new_comment.txt').render(
            Context({
                'comment': instance,
                'site': site,
            }))
        send_mail(
            ugettext(u'New comment under your story at %s.') % site.domain,
            mail_text, settings.SERVER_EMAIL, 
            [instance.content_object.author_email]
        )
models.signals.post_save.connect(notify_new_comment, sender=XtdComment)