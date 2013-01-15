from django.forms import ModelForm
from .models import Question

class QuestionForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Question
        fields = ['email', 'question']

    def save(self, *args, **kwargs):
        instance = super(QuestionForm, self).save(*args, **kwargs)
        instance.ack_author()
        return instance
