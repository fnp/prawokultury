from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField
from fnpdjango.utils.models.translation import add_translatable


class Chunk(models.Model):
    """
    A Chunk is a piece of content associated with a unique key that can be inserted into
    any template with the use of a special template tag.
    """
    key = models.CharField(_('key'), help_text=_('A unique name for this chunk of content'), primary_key=True, max_length=255)
    description = models.CharField(_('description'), blank=True, max_length=255)

    class Meta:
        ordering = ('key',)
        verbose_name = _('chunk')
        verbose_name_plural = _('chunks')

    def __unicode__(self):
        return self.key

    def cache_key(self):
        return 'chunk_' + self.key

    def save(self, *args, **kwargs):
        ret = super(Chunk, self).save(*args, **kwargs)
        cache.delete(self.cache_key())
        return ret

add_translatable(Chunk, {
    'content': MarkupField(_('content'), blank=True, markup_type='textile_pl',
        help_text=_('Use <a href="http://txstyle.org/">Textile</a> syntax.')),
})


class Attachment(models.Model):
    key = models.CharField(_('key'), help_text=_('A unique name for this attachment'), primary_key=True, max_length=255)
    attachment = models.FileField(upload_to='chunks/attachment')

    class Meta:
        ordering = ('key',)
        verbose_name, verbose_name_plural = _('attachment'), _('attachments')

    def __unicode__(self):
        return self.key
