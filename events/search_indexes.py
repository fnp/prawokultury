import datetime
from django.conf import settings
from haystack import indexes
from fnpdjango.utils.models.translation import add_translatable_index, localize_field
from events.models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(null=True,
        model_attr=localize_field('title', settings.LANGUAGE_CODE),
        document=True)

    def get_model(self):
        return Event


add_translatable_index(EventIndex, {
    'organizer': indexes.CharField(null=True),
    'place': indexes.CharField(null=True)
    })

add_translatable_index(EventIndex, {
    'title': indexes.CharField(null=True),
    }, 
    (lang for lang in settings.LANGUAGES if lang[0] != settings.LANGUAGE_CODE)
)
