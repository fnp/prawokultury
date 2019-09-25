# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django import forms
from django.core.mail import send_mail

from contact.forms import ContactForm
from contact.models import Contact
from contact.fields import HeaderField
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from migdal.models import Entry

from prawokultury.countries import COUNTRIES, TRAVEL_GRANT_COUNTRIES

mark_safe_lazy = lazy(mark_safe, unicode)


class RegistrationForm(ContactForm):
    form_tag = 'register'

    save_as_tag = '2019'
    conference_name = u'CopyCamp 2019'
    notify_on_register = False
    
    form_title = _('Registration')
    admin_list = ['first_name', 'last_name', 'organization']

    first_name = forms.CharField(label=_('First name'), max_length=128)
    last_name = forms.CharField(label=_('Last name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'), max_length=256, required=False)
    agree_license = forms.BooleanField(
        label=_('Permission for publication'),
        help_text=mark_safe_lazy(_(
            u'I agree to having materials, recorded during the conference, released under the terms of '
            u'<a href="http://creativecommons.org/licenses/by-sa/3.0/deed">CC\u00a0BY-SA</a> license and '
            u'to publishing my image.')),
        required=False
    )
    agree_terms = forms.BooleanField(
        label=mark_safe_lazy(
            _(u'I accept <a href="/en/info/terms-and-conditions/">CopyCamp Terms and Conditions</a>.'))
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.started = getattr(settings, 'REGISTRATION_STARTED', False)
        self.limit_reached = Contact.objects.filter(form_tag=self.save_as_tag).count() >= settings.REGISTRATION_LIMIT

    def main_fields(self):
        return [self[name] for name in (
            'first_name', 'last_name', 'contact', 'organization')]

    def survey_fields(self):
        return []

    def agreement_fields(self):
        return [self[name] for name in ('agree_license', 'agree_toc')]


class RegisterSpeaker(RegistrationForm):
    form_tag = 'register-speaker'
    save_as_tag = '2019-speaker'
    form_title = _('Open call for presentations')
    notify_on_register = False
    mailing_field = 'agree_mailing'

    bio = forms.CharField(label=mark_safe_lazy(
        _('Short biographical note in Polish (max. 500 characters)')),
                          widget=forms.Textarea, max_length=500, required=True)
    bio_en = forms.CharField(label=_('Short biographical note in English (max. 500 characters, not required)'), widget=forms.Textarea,
                             max_length=500, required=False)
    photo = forms.FileField(label=_('Photo'), required=False)
    phone = forms.CharField(label=_('Phone number'), max_length=64,
                            required=False,
                            help_text=_('(used only for organizational purposes)'))

    presentation_title = forms.CharField(
        label=mark_safe_lazy(_('Presentation title in Polish')),
        max_length=256)
    presentation_title_en = forms.CharField(
        label=_('Presentation title in English (not required)'), max_length=256, required=False)
    presentation_summary = forms.CharField(label=_('Presentation summary (max. 1800 characters)'),
                                           widget=forms.Textarea, max_length=1800)

    # presentation_post_conference_publication = forms.BooleanField(
    #     label=_('I am interested in including my paper in the post-conference publication'),
    #     required=False
    # )

    agree_data = None

    def __init__(self, *args, **kw):
        super(RegisterSpeaker, self).__init__(*args, **kw)
        self.started = getattr(settings, 'REGISTRATION_SPEAKER_STARTED', False)
        self.closed = getattr(settings, 'REGISTRATION_SPEAKER_CLOSED', False)
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'contact',
            'phone',
            'organization',
            'bio',
            'bio_en',
            'photo',
            'presentation_title',
            'presentation_title_en',
            'presentation_summary',

            'agree_license',
            'agree_terms',
        ]


class RemindForm(ContactForm):
    form_tag = 'remind-me'
    save_as_tag = 'remind-me-2019'
    form_title = u'CopyCamp 2019'
    notify_on_register = False
    notify_user = False


class NextForm(ContactForm):
    form_tag = '/next'
    form_title = _('Next CopyCamp')

    name = forms.CharField(label=_('Name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'),
                                   max_length=256, required=False)


def workshop_field(label, help=None):
    return forms.BooleanField(label=_(label), required=False, help_text=help)


class WorkshopForm(ContactForm):
    form_tag = 'workshops'
    save_as_tag = 'workshops-2018'
    conference_name = u'CopyCamp 2018'
    form_title = _('Workshop')
    notify_on_register = False
    mailing_field = 'agree_mailing'

    first_name = forms.CharField(label=_('First name'), max_length=128)
    last_name = forms.CharField(label=_('Last name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'), max_length=256, required=False)
    country = forms.ChoiceField(
        label=_('Country of residence'), choices=[('', '--------')] + zip(COUNTRIES, COUNTRIES), required=False)

    _header = HeaderField(
        label=mark_safe_lazy(_("<h3>I'll take a part in workshops</h3>")),
        help_text=_('Only workshops with any spots left are visible here.'))

    _h1 = HeaderField(label=mark_safe_lazy(_("<strong>Friday, October 5th, 11 a.m.–1 p.m.</strong>")))

    w_dobosz = workshop_field(
        u'Elżbieta Dobosz, Urząd Patentowy RP: Ochrona wzornictwa, co można chronić, co warto chronić i w jaki sposób',
        u'Uczestnicy mogą przedstawić na warsztatach swoje wzory – '
        u'rozwiązania wizualne ze wszystkich kategorii produktów.')
    w_kozak = workshop_field(
        u'Łukasz Kozak i Krzysztof Siewicz: Projekt : Upiór – wprowadzenie i warsztaty dla twórców gier')
    w_secker = workshop_field(
        u'Jane Secker and Chris Morrison: Embedding Copyright literacy using games-based learning',
        _(u'The workshop will be conducted in English.'))

    _h2 = HeaderField(label=mark_safe_lazy(_("<strong>Saturday, October 6th, 11 a.m.–1 p.m.</strong>")))

    w_kakareko = workshop_field(
        u'Ksenia Kakareko: Regulacje prawne dotyczące wykorzystania materiałów zdigitalizowanych')
    w_kakareko_question = forms.CharField(
        label=u'Możesz opisać sprawy, z którymi najczęściej spotykasz się jako pracownik instytucji posiadającej '
              u'zdigitalizowane zbiory lub jako użytkownik tych zbiorów '
              u'(max 800 znaków)',
        max_length=800, widget=forms.Textarea, required=False)
    w_sikorska = workshop_field(
        u'Krzysztof Siewicz: Autor: projektant / prawo autorskie dla projektantów')
    w_sikorska_question = forms.CharField(
        label=u'Jeżeli chcesz, możesz przesłać prowadzącemu swoje pytanie dotyczące prawa autorskiego, '
              u'co pomoże mu lepiej przygotować warsztaty '
              u'(max 800 znaków)',
        max_length=800, widget=forms.Textarea, required=False)
    w_sztoldman = workshop_field(
        u'dr Agnieszka Sztoldman, Aleksandra Burda, SMM Legal: Spory o pieniądze w branżach IP-driven')

    _header_1 = HeaderField(label='')
    _header_2 = HeaderField(label='')

    start_workshops = ('dobosz', 'kozak', 'secker', 'kakareko', 'sikorska', 'sztoldman')

    slots = (
        ('_h1', 'dobosz', 'kozak', 'secker'),
        ('_h2', 'kakareko', 'sikorska', 'sztoldman'),
    )

    limits = {
        'dobosz': 30,
        'kozak': 30,
        'secker': 30,
        'kakareko': 30,
        'sikorska': 30,
        'sztoldman': 30,
    }

    agree_mailing = forms.BooleanField(
        label=_('I am interested in receiving information about the Modern Poland Foundation\'s activities by e-mail'),
        required=False)
    agree_license = forms.BooleanField(
        label=_('Permission for publication'),
        help_text=mark_safe_lazy(_(
            u'I agree to having materials, recorded during the conference, released under the terms of '
            u'<a href="http://creativecommons.org/licenses/by-sa/3.0/deed">CC\u00a0BY-SA</a> '
            u'license and to publishing my image.')),
        required=False)

    def __init__(self, *args, **kwargs):
        super(WorkshopForm, self).__init__(*args, **kwargs)
        try:
            url = Entry.objects.get(slug_pl='regulamin').get_absolute_url()
            self.fields['agree_toc'] = forms.BooleanField(
                required=True,
                label=mark_safe(_('I accept <a href="%s">Terms and Conditions of CopyCamp</a>') % url)
            )
        except Entry.DoesNotExist:
            pass
        counts = {k: 0 for k in self.start_workshops}
        for contact in Contact.objects.filter(form_tag=self.save_as_tag):
            for workshop in self.start_workshops:
                if contact.body.get('w_%s' % workshop, False):
                    counts[workshop] += 1
                    # if workshop == 'youtube' and counts[workshop] == 30:
                    #     send_mail(u'Warsztaty YouTube', u'Przekroczono limit 30 osób na warsztaty YouTube',
                    #               'no-reply@copycamp.pl',
                    #               ['krzysztof.siewicz@nowoczesnapolska.org.pl'],
                    #               fail_silently=True)

        some_full = False
        for k, v in counts.items():
            if v >= self.limits[k]:
                some_full = True
                if 'w_%s' % k in self.fields:
                    del self.fields['w_%s' % k]
        if not some_full:
            self.fields['_header'].help_text = None

    def clean(self):
        for slot in self.slots:
            if sum(1 for w in slot if self.cleaned_data.get('w_%s' % w)) > 1:
                self._errors[slot[0]] = [_("You can't choose more than one workshop during the same period")]
        if not any(self.cleaned_data.get('w_%s' % w) for w in self.start_workshops):
            self._errors['_header'] = [_("Please choose at least one workshop.")]
        return self.cleaned_data
