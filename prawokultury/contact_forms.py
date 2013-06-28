# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from contact.forms import ContactForm
from contact.models import Contact
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(ContactForm):
    form_tag = 'register'
    form_title = _('Take part!')
    admin_list = ['name', 'organization', 'title']

    name = forms.CharField(label=_('Name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'), 
            max_length=256, required=False)
    title = forms.CharField(label=_('Title of presentation'), 
            max_length=256, required=False)
    presentation = forms.FileField(label=_('Presentation'),
            required=False)
    summary = forms.CharField(label=_('Summary of presentation (max. 1800 characters)'),
            widget=forms.Textarea, max_length=1800, required=False)
    agree_data = forms.BooleanField(
        label=_('Permission for data processing'),
        help_text=_(u'I hereby grant Modern Poland Foundation (Fundacja Nowoczesna Polska, ul. Marszałkowska 84/92, 00-514 Warszawa) permission to process my personal data (name, e-mail address) for purposes of registration for CopyCamp conference.')
    )
    agree_license = forms.BooleanField(
        label=_('Permission for publication'),
        help_text=_('I agree to having materials recorded during the conference released under the terms of <a href="http://creativecommons.org/licenses/by-sa/3.0/deed">CC BY-SA</a> license.')
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.limit_reached = Contact.objects.filter(form_tag=self.form_tag).count() >= settings.REGISTRATION_LIMIT
        if self.limit_reached:
            for field in ('title', 'summary'):
                self.fields[field].required = True
