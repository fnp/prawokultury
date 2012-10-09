from django.conf import settings
import datetime
from haystack import indexes
from events.models import Event
from fnpdjango.utils.models.translation import add_translatable_index


class EventIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    def get_model(self):
        return Event

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


add_translatable_index(EventIndex, {
# Haystack needs a main field to be the same across all indexes
# so we treat title of the event as this main content, named 'body'
   'body': indexes.CharField(model_attr='title', null=True),
   'organizer': indexes.CharField(null=True),
   'place': indexes.CharField(null=True)
   })


getattr(EventIndex, "body_%s" % settings.LANGUAGE_CODE).document = True
