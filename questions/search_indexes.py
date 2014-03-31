import datetime
from django.conf import settings
from haystack import indexes
from .models import Question


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    answer = indexes.CharField(model_attr="answer")

    def prepare_text(self, obj):
        return unicode(obj)

    def get_model(self):
        return Question

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(published=True)
