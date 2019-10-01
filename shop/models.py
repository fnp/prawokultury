# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from datetime import datetime
from django.core.mail import send_mail, mail_managers
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, override
import getpaid
from migdal.models import Entry
from . import app_settings


class Offer(models.Model):
    """ A fundraiser for a particular book. """
    entry = models.OneToOneField(Entry, models.CASCADE)  # filter publications!
    price = models.DecimalField(_('price'), decimal_places=2, max_digits=6)
    cost_const = models.DecimalField(decimal_places=2, max_digits=6)
    cost_per_item = models.DecimalField(decimal_places=2, max_digits=6, default=0)

    class Meta:
        verbose_name = _('offer')
        verbose_name_plural = _('offers')
        ordering = ['entry']

    def __unicode__(self):
        return unicode(self.entry)

    def get_absolute_url(self):
        return self.entry.get_absolute_url()

    def total_per_item(self):
        return self.price + self.cost_per_item

    def price_per_items(self, items):
        return self.cost_const + items * self.total_per_item()


class Order(models.Model):
    """ A person paying for a book.

    The payment was completed if and only if payed_at is set.

    """
    offer = models.ForeignKey(Offer, models.CASCADE, verbose_name=_('offer'))
    items = models.IntegerField(verbose_name=_('items'), default=1)
    name = models.CharField(_('name'), max_length=127, blank=True)
    email = models.EmailField(_('email'), db_index=True)
    address = models.TextField(_('address'), db_index=True)
    payed_at = models.DateTimeField(_('payed at'), null=True, blank=True, db_index=True)
    language_code = models.CharField(max_length = 2, null = True, blank = True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-payed_at']

    def __unicode__(self):
        return "%s (%d egz.)" % (unicode(self.offer), self.items)

    def get_absolute_url(self):
        return self.offer.get_absolute_url()

    def amount(self):
        return self.offer.price_per_items(self.items)

    def notify(self, subject, template_name, extra_context=None):
        context = {
            'order': self,
            'site': Site.objects.get_current(),
        }
        if extra_context:
            context.update(extra_context)
        with override(self.language_code or app_settings.DEFAULT_LANGUAGE):
            send_mail(subject,
                render_to_string(template_name, context),
                getattr(settings, 'CONTACT_EMAIL', 'prawokultury@nowoczesnapolska.org.pl'),
                [self.email],
                fail_silently=False
            )

    def notify_managers(self, subject, template_name, extra_context=None):
        context = {
            'order': self,
            'site': Site.objects.get_current(),
        }
        if extra_context:
            context.update(extra_context)
        with override(app_settings.DEFAULT_LANGUAGE):
            mail_managers(subject, render_to_string(template_name, context))

# Register the Order model with django-getpaid for payments.
getpaid.register_to_payment(Order, unique=False, related_name='payment')


def new_payment_query_listener(sender, order=None, payment=None, **kwargs):
    """ Set payment details for getpaid. """
    payment.amount = order.amount()
    payment.currency = 'PLN'
getpaid.signals.new_payment_query.connect(new_payment_query_listener)


def user_data_query_listener(sender, order, user_data, **kwargs):
    """ Set user data for payment. """
    user_data['email'] = order.email
getpaid.signals.user_data_query.connect(user_data_query_listener)

def payment_status_changed_listener(sender, instance, old_status, new_status, **kwargs):
    """ React to status changes from getpaid. """
    if old_status != 'paid' and new_status == 'paid':
        instance.order.payed_at = datetime.now()
        instance.order.save()
        instance.order.notify(
            _('Your payment has been completed.'),
            'shop/email/payed.txt'
        )
        instance.order.notify_managers(
            _('New order has been placed.'),
            'shop/email/payed_managers.txt'
        )
getpaid.signals.payment_status_changed.connect(payment_status_changed_listener, dispatch_uid='shop.models.payment_status_changed_listener')
