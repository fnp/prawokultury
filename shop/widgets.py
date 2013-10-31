from django.forms.widgets import TextInput

class NumberInput(TextInput):
    input_type = 'number'
