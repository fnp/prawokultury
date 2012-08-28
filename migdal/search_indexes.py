from django.conf import settings
import datetime
from haystack import indexes
from migdal.models import Entry
from migdal.helpers import add_translatable_index


class EntryIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(indexed=True, model_attr="date")
    author = indexes.CharField(model_attr="author")

    def get_model(self):
        return Entry

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all() # from example: filter(date__lte=datetime.datetime.now())


add_translatable_index(EntryIndex, {
    'title': indexes.CharField(),
    'lead': indexes.CharField(),
    'body': indexes.CharField()
    })


getattr(EntryIndex, "body_%s" % settings.LANGUAGE_CODE).document = True
