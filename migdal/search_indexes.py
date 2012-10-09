import datetime
from django.conf import settings
from haystack import indexes
from fnpdjango.utils.models.translation import add_translatable_index
from migdal.models import Entry


class EntryIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(indexed=True, model_attr="date")
    author = indexes.CharField(model_attr="author")

    def get_model(self):
        return Entry

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()  # filter(date__lte=datetime.datetime.now())


add_translatable_index(EntryIndex, {
    'title': indexes.CharField(null=True),
    'lead': indexes.CharField(null=True),
    'body': indexes.CharField(null=True)
    })


getattr(EntryIndex, "body_%s" % settings.LANGUAGE_CODE).document = True
