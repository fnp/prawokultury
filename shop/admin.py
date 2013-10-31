# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import Offer, Order


class OfferAdmin(admin.ModelAdmin):
    model = Offer
    list_display = ['entry', 'price']


class PayedFilter(admin.SimpleListFilter):
    title = _('payment complete')
    parameter_name = 'payed'
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(payed_at=None)
        elif self.value() == 'no':
            return queryset.filter(payed_at=None)

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['payed_at', 'offer', 'name', 'email']
    search_fields = ['name', 'email', 'offer']
    list_filter = [PayedFilter, 'offer']

admin.site.register(Offer, OfferAdmin)
admin.site.register(Order, OrderAdmin)
