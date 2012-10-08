from django import forms
from contact.forms import ContactForm
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(ContactForm):
    form_tag = 'register'
    name = forms.CharField(label=_('Name'), max_length=128)
    organization = forms.CharField(label=_('Organization'), max_length=128)
    summary = forms.CharField(label=_('Summary'), widget=forms.Textarea)
    presentation = forms.FileField(label=_('Presentation'))
