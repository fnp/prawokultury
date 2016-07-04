from django import forms
from django.forms.util import flatatt
from django.utils.html import format_html

class HeaderWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        return ''
        attrs.update(self.attrs)
        return format_html('<div{0}>{1}</div>', flatatt(attrs), unicode(value))

