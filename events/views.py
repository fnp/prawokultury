from datetime import datetime
from django.shortcuts import render
from events.models import Event


def events(request):
    events = Event.objects.filter(date__gte=datetime.now())
    events = events.filter(**{"published_%s" % request.LANGUAGE_CODE: True})
    return render(request, 'events/event_list.html', {
        'object_list': events,
    })


def events_past(request):
    events = Event.objects.filter(date__lte=datetime.now()).order_by('-date')
    events = events.filter(**{"published_%s" % request.LANGUAGE_CODE: True})
    return render(request, 'events/event_list.html', {
        'object_list': events,
        'past': True,
    })
