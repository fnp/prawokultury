# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django import template
from shop.forms import OrderForm

register = template.Library()


@register.inclusion_tag('shop/snippets/order_form.html', takes_context=True)
def order_form_for(context, offer, form=None):
    if form is None:
        form = OrderForm(offer)
    return {'form': form}
