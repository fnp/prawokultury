# -*- coding: utf-8
from datetime import datetime
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField

class Question(models.Model):
    email = models.EmailField(_('contact e-mail'), null=True, blank=True)
    question = models.TextField(_('question'), db_index=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    changed_at = models.DateTimeField(_('changed at'), auto_now=True)
    approved = models.BooleanField(_('approved'), default=False)
    edited_question = models.TextField(_('edited question'), db_index=True, null=True, blank=True,
            help_text=_("Leave empty if question doesn't need editing."))
    answer = MarkupField(_('answer'), markup_type='textile_pl', blank=True,
            help_text=_('Use <a href="http://textile.thresholdstate.com/">Textile</a> syntax.'))
    answered = models.BooleanField(_('answered'), db_index=True, default=False,
            help_text=_('Check to send the answer to user.'))
    answered_at = models.DateTimeField(_('answered at'), null=True, blank=True, db_index=True)
    published = models.BooleanField(_('published'), db_index=True, default=False,
        help_text=_('Check to display answered question on site.'))
    published_at = models.DateTimeField(_('published at'), null=True, blank=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return self.edited_question or self.question

    @models.permalink
    def get_absolute_url(self):
        return ('questions_question', (self.pk,))

    def notify_author(self):
        if not self.email:
            return
        site = Site.objects.get_current()
        context = Context({
                'question': self,
                'site': site,
            })
        text_content = loader.get_template('questions/answered_mail.txt'
            ).render(context)
        html_content = loader.get_template('questions/answered_mail.html'
            ).render(context)
        msg = EmailMultiAlternatives(
            u'Odpowiedź na Twoje pytanie w serwisie %s.' % site.domain,
            text_content, settings.SERVER_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def save(self, *args, **kwargs):
        now = datetime.now()
        if self.answered and not self.answered_at:
            self.notify_author()
            self.answered_at = now
        if self.published and not self.published_at:
            self.published_at = now
        super(Question, self).save(*args, **kwargs)
