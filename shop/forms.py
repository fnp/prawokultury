# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django import forms
from django.utils import formats
from django.utils.translation import ugettext_lazy as _, ugettext, get_language
from . import app_settings
from .models import Order
from .widgets import NumberInput


class OrderForm(forms.Form):
    required_css_class = 'required'
    backend = 'getpaid.backends.payu'
    items = forms.IntegerField(label=_("Items"), min_value=1, initial=1,
        widget=NumberInput(attrs={'min': '1', 'step': '1', 'class': 'cost-items'}))
    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("Contact e-mail"))
    address = forms.CharField(label=_("Shipping address"), widget=forms.Textarea)

    accept = forms.BooleanField(label=_("Accept terms"),
        help_text='''Akceptuję <a href='/info/regulamin-sklepu/'>regulamin sklepu</a>.''')

    consent = forms.BooleanField(label=_("Consent to the processing of data"),
        help_text='''Wyrażam zgodę na przetwarzanie moich danych osobowych w celu realizacji
zamówienia. Administratorem danych osobowych jest Fundacja Nowoczesna
Polska, ul. Marszałkowska 84/92, lok. 125, 00-514 Warszawa.
Zapoznałem/zapoznałam się
z&nbsp;<a href="http://nowoczesnapolska.org.pl/prywatnosc/">polityką prywatności Fundacji</a>.
Jestem świadom/świadoma, iż moja zgoda może być odwołana w każdym czasie, co skutkować będzie
usunięciem mojego adresu e-mail z bazy danych.''')

    def __init__(self, offer, *args, **kwargs):
        self.offer = offer
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['items'].widget.attrs.update({
            'data-cost-price': self.offer.price,
            'data-cost-per-item': self.offer.cost_per_item,
            'data-cost-const': self.offer.cost_const,
            'data-decimal-separator': formats.get_format("DECIMAL_SEPARATOR"),
            })

    def save(self):
        order = Order.objects.create(
            offer=self.offer,
            items=self.cleaned_data['items'],
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            address=self.cleaned_data['address'],
            language_code = get_language(),
        )
        return order

