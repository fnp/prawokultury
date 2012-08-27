from datetime import datetime
from django.shortcuts import render
from events.models import Event


def events(request):
    return render(request, 'events/event_list.html', {
        'object_list': Event.objects.filter(date__gte=datetime.now())
    })


def events_past(request):
    return render(request, 'events/event_list.html', {
        'object_list': Event.objects.filter(date__lte=datetime.now()
            ).order_by('-date'),
        'past': True,
    })
