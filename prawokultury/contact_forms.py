from django import forms
from contact.forms import ContactForm
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(ContactForm):
    form_tag = 'register'
    title = _('Registration form')

    name = forms.CharField(label=_('Name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'), 
            max_length=256, required=False)
    title = forms.CharField(label=_('Title of presentation'), 
            max_length=256, required=False)
    presentation = forms.FileField(label=_('Presentation'),
            required=False)
    summary = forms.CharField(label=_('Summary'),
            widget=forms.Textarea, required=False)
