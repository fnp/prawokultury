# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from prawokultury.contact_forms import RegistrationForm
from .contact_forms import RegisterSpeaker


def registration_url(request):
    speaker_form = RegisterSpeaker()
    registration_form = RegistrationForm()
    if speaker_form.started and not speaker_form.closed:
        url = reverse("contact_form", args=["register-speaker"])
    elif speaker_form.closed and not registration_form.started:
        url = reverse("contact_form", args=["remind-me"])
    else:
        url = reverse("contact_form", args=["register"])
    return {'REGISTRATION_URL': url}
