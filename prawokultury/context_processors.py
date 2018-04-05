# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from prawokultury.contact_forms import RegistrationForm
from .contact_forms import RegisterSpeaker


def registration_url(request):
    speaker_form = RegisterSpeaker()
    registration_form = RegistrationForm()
    if speaker_form.started and not speaker_form.closed:
        url = reverse("contact_form", args=["register-speaker"])
        label = _('Registration')
    elif speaker_form.closed and not registration_form.started:
        url = reverse("contact_form", args=["remind-me"])
        label = _('Remind me')
    else:
        url = reverse("contact_form", args=["register"])
        label = _('Registration')
    return {'REGISTRATION_URL': url, 'REGISTRATION_BUTTON_LABEL': label}
