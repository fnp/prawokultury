# -*- coding: utf-8 -*-
import random
import string
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from . import app_settings


class Contact(models.Model):
    created_at = models.DateTimeField(_('submission date'), auto_now_add=True)
    ip = models.IPAddressField(_('IP address'), default='127.0.0.1')
    contact = models.CharField(_('contact'), max_length=128)
    form_tag = models.CharField(_('form'), max_length=32, db_index=True)
    body = JSONField(_('body'))
    key = models.CharField(_('key'), max_length=64, db_index=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('submitted form')
        verbose_name_plural = _('submitted forms')

    def __unicode__(self):
        return unicode(self.created_at)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Contact, self).save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        key = ''
        while not key or key in [record['key'] for record in cls.objects.values('key')]:
            key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(30))
        return key


class Attachment(models.Model):
    contact = models.ForeignKey(Contact)
    tag = models.CharField(max_length=64)
    file = models.FileField(upload_to='contact/attachment')

    @models.permalink
    def get_absolute_url(self):
        return ('contact_attachment', [self.contact_id, self.tag])


__import__(app_settings.FORMS_MODULE)
