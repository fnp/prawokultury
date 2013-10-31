# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from datetime import date
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView, DetailView, ListView
import getpaid.backends.payu
from getpaid.models import Payment
from . import app_settings
from .forms import OrderForm
from .models import Offer, Order



class OfferDetailView(FormView):
    form_class = OrderForm
    template_name = "shop/offer_detail.html"
    backend = 'getpaid.backends.payu'

    @csrf_exempt
    def dispatch(self, request, slug):
        if getattr(self, 'object', None) is None:
            lang = request.LANGUAGE_CODE
            args = {'entry__slug_%s' % lang: slug}
            self.object = get_object_or_404(Offer, **args)
        return super(OfferDetailView, self).dispatch(request, slug)

    def get(self, *args, **kwargs):
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, *args, **kwargs):
        ctx = super(OfferDetailView, self).get_context_data(*args, **kwargs)
        ctx['entry'] = self.object.entry
        return ctx

    def get_form(self, form_class):
        return form_class(self.object, self.request.POST)

    def form_valid(self, form):
        order = form.save()
        # Skip getpaid.forms.PaymentMethodForm, go directly to the broker.
        payment = Payment.create(order, self.backend)
        gateway_url_tuple = payment.get_processor()(payment).get_gateway_url(self.request)
        payment.change_status('in_progress')
        return redirect(gateway_url_tuple[0])


class ThanksView(DetailView):
    model = Payment
    template_name = "shop/thanks.html"


class NoThanksView(DetailView):
    model = Payment
    template_name = "shop/no_thanks.html"
