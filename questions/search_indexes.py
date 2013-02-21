import datetime
from django.conf import settings
from haystack import indexes
from .models import Question


class QuestionIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr="__unicode__")
    answer = indexes.CharField(model_attr="answer")

    def get_model(self):
        return Question

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(published=True)
