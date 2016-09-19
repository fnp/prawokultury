# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from .contact_forms import RegisterSpeaker


def registration_url(request):
    speaker_form = RegisterSpeaker()
    if speaker_form.started and not speaker_form.closed:
        url = reverse("contact_form", args=["register-speaker"])
    else:
        url = reverse("contact_form", args=["register"])
    return {'REGISTRATION_URL': url}
