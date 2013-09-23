# -*- coding: utf-8 -*-
# This file is part of Wolnelektury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django import forms
from django.utils import formats
from django.utils.translation import ugettext_lazy as _, ugettext, get_language
from .models import Order
from . import app_settings


class OrderForm(forms.Form):
    required_css_class = 'required'
    backend = 'getpaid.backends.payu'

    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("Contact e-mail"))
    address = forms.CharField(label=_("Address"), widget=forms.Textarea)
    consent = forms.CharField(label=_("Consent"), widget=forms.Textarea,
        help_text=_('I hereby consent'))

    def __init__(self, offer, *args, **kwargs):
        print 'o:', offer
        self.offer = offer
        super(OrderForm, self).__init__(*args, **kwargs)

    def save(self):
        order = Order.objects.create(
            offer=self.offer,
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            address=self.cleaned_data['address'],
            language_code = get_language(),
        )
        return order

