import datetime
from haystack import indexes
from migdal.models import Entry
from django.conf import settings
from copy import copy


class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    date = indexes.DateTimeField(indexed=True)
    author = indexes.CharField()

    def get_model(self):
        return Entry

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date__lte=datetime.datetime.now())


def add_translatable(index_class, fields, languages=None):
    """Adds some translatable fields to a search index, and a getter."""
    if languages is None:
        languages = settings.LANGUAGES
    for name, field in fields.items():
        for lang_code, lang_name in languages:
            new_field = copy(field)
            fname = "%s_%s" % (name, lang_code)
            new_field.index_fieldname = fname
            setattr(index_class, fname, new_field)
            index_class.fields[fname] = new_field


add_translatable(EntryIndex, {
    'title': indexes.CharField(indexed=True, document=False),
    'lead': indexes.CharField(indexed=True, document=False),
    'body': indexes.CharField(indexed=True, document=False)
    })


getattr(EntryIndex, "body_%s" % settings.LANGUAGE_CODE).document = True
