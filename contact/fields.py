from django import forms
from .widgets import HeaderWidget

class HeaderField(forms.CharField):
    def __init__(self, required=False, widget=None, *args, **kwargs):
        if widget is None:
            widget = HeaderWidget
        super(HeaderField, self).__init__(required=required, widget=widget, *args, **kwargs)

