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

    save_as_tag = '2018'
    conference_name = u'CopyCamp 2018'
    notify_on_register = False
    
    form_title = _('Registration')
    admin_list = ['first_name', 'last_name', 'organization']

    mailing_field = 'agree_mailing'

    travel_grant_countries = TRAVEL_GRANT_COUNTRIES

    first_name = forms.CharField(label=_('First name'), max_length=128)
    last_name = forms.CharField(label=_('Last name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'), max_length=256, required=False)
    country = forms.ChoiceField(
        label=_('Country of residence'), choices=[('', '--------')] + zip(COUNTRIES, COUNTRIES), required=False)
    travel_grant = forms.BooleanField(
        label=_('I require financial assistance to attend CopyCamp 2018.'), required=False)
    travel_grant_motivation = forms.CharField(
        label=_('Please write us about yourself and why you want to come to CopyCamp. '
                'This information will help us evaluate your travel grant application:'),
        help_text=_('Financial assistance for German audience is possible '
                    'thanks to the funds of the German Federal Foreign Office transferred by '
                    'the Foundation for Polish-German Cooperation.'),
        widget=forms.Textarea, max_length=600, required=False)

    days = forms.ChoiceField(
       label=_("I'm planning to show up on"),
       choices=[
           ('both', _('Both days of the conference')),
           ('only-28th', _('October 5th only')),
           ('only-29th', _('October 6th only')),
       ], widget=forms.RadioSelect())

    # ankieta
    times_attended = forms.ChoiceField(
        required=False,
        label=_("1. How many times have you attended CopyCamp?"),
        choices=[
            ('0', _('not yet')),
            ('1', _('once')),
            ('2', _('twice')),
            ('3', _('three times')),
            ('4', _('four times')),
            ('5', _('five times')),
        ], widget=forms.RadioSelect())
    age = forms.ChoiceField(
        required=False,
        label=_("2. Please indicate your age bracket:"),
        choices=[
            ('0-19', _('19 or below')),
            ('20-25', _('20-25')),
            ('26-35', _('26-35')),
            ('36-45', _('36-45')),
            ('46-55', _('46-55')),
            ('56-65', _('56-65')),
            ('66+', _('66 or above')),
        ], widget=forms.RadioSelect())
    areas = forms.MultipleChoiceField(
        required=False,
        label=_("3. Please indicate up to 3 areas you feel most affiliated with"),
        choices=[
            ('sztuki plastyczne', _('visual art')),
            ('literatura', _('literature')),
            ('muzyka', _('music')),
            ('teatr', _('theatre')),
            ('film', _('film production')),
            ('wydawanie', _('publishing')),
            ('prawo', _('law')),
            ('ekonomia', _('economy')),
            ('socjologia', _('sociology')),
            ('technika', _('technology')),
            ('edukacja', _('education')),
            ('studia', _('higher education')),
            ('nauka', _('academic research')),
            ('biblioteki', _('library science')),
            ('administracja', _('public administration')),
            ('ngo', _('nonprofit organisations')),
            ('other', _('other (please specify below)')),
        ], widget=forms.CheckboxSelectMultiple())
    areas_other = forms.CharField(required=False, label=_('Fill if you selected “other” above'))
    source = forms.ChoiceField(
        required=False,
        label=_("4. Please indicate how you received information about the conference:"),
        choices=[
            ('znajomi', _('through friends sharing on the web')),
            ('znajomi2', _('through friends by other means')),
            ('prasa', _('through press')),
            ('fnp', _('directly through the Foundation\'s facebook or website')),
            ('www', _('through other websites (please specify below)')),
            ('other', _('other (please specify below)')),
        ], widget=forms.RadioSelect())
    source_other = forms.CharField(required=False, label=_('Fill if you selected “other” or “other website” above'))
    motivation = forms.ChoiceField(
        required=False,
        label=_("6. Please indicate the most important factor for your willingness to participate:"),
        choices=[
            ('speaker', _('listening to particular speaker(s)')),
            ('networking', _('good networking occasion')),
            ('partnering', _('partnering with organisations present at the event')),
            ('other', _('other (please specify below)')),
        ], widget=forms.RadioSelect())
    motivation_other = forms.CharField(required=False, label=_('Fill if you selected “other” above'))

    agree_mailing = forms.BooleanField(
        label=_('I want to receive e-mails about future CopyCamps '
                'and similar activities of the Modern Poland Foundation'),
        required=False
    )
    agree_license = forms.BooleanField(
        label=_('Permission for publication'),
        help_text=mark_safe_lazy(_(
            u'I agree to having materials, recorded during the conference, released under the terms of '
            u'<a href="http://creativecommons.org/licenses/by-sa/3.0/deed">CC\u00a0BY-SA</a> license and '
            u'to publishing my image.')),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.started = getattr(settings, 'REGISTRATION_STARTED', False)
        self.limit_reached = Contact.objects.filter(form_tag=self.save_as_tag).count() >= settings.REGISTRATION_LIMIT
        try:
            url = Entry.objects.get(slug_pl='regulamin').get_absolute_url()
            self.fields['agree_toc'] = forms.BooleanField(
                required=True,
                label=mark_safe(_('I accept <a href="%s">Terms and Conditions of CopyCamp</a>') % url)
            )
        except Entry.DoesNotExist:
            pass

    def clean_areas(self):
        data = self.cleaned_data['areas']
        if len(data) > 3:
            raise forms.ValidationError(_('Select at most 3 areas'))
        return data

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'travel_grant' in cleaned_data:
            country = cleaned_data['country']
            travel_grant = cleaned_data['travel_grant']
            motivation = cleaned_data['travel_grant_motivation']
            if country not in self.travel_grant_countries and travel_grant:
                raise forms.ValidationError(_('Travel grant is not provided for the selected country'))
            if travel_grant and not motivation:
                self._errors['travel_grant_motivation'] = _('Please provide this information')
                raise forms.ValidationError(_('To apply for a travel grant you must provide additional information.'))
            if not travel_grant and motivation:
                cleaned_data['motivation'] = ''
        return cleaned_data

    def main_fields(self):
        return [self[name] for name in (
            'first_name', 'last_name', 'contact', 'organization', 'country',
            'travel_grant', 'travel_grant_motivation', 'days')]

    def survey_fields(self):
        return [self[name] for name in (
            'times_attended', 'age',
            'areas', 'areas_other', 'source', 'source_other', 'motivation', 'motivation_other')]

    def agreement_fields(self):
        return [self[name] for name in ('agree_mailing', 'agree_license', 'agree_toc')]


tracks = (
    _('social security in the creative sector'),
    _('100 years of the evolution of modern copyright law and industrial property law in Poland '
      'and of cultural activities regulated by this law'),
    _('EU copyright reform'),
    _('blockchain use prospects'),
    _('reuse of archives and cultural heritage'),
)


class RegisterSpeaker(RegistrationForm):
    form_tag = 'register-speaker'
    save_as_tag = '2018-speaker'
    form_title = _('Open call for presentations')
    notify_on_register = False
    mailing_field = 'agree_mailing'

    presentation_thematic_track = forms.ChoiceField(
        label=_('Thematic track'),
        choices=[(t, t) for t in tracks], widget=forms.RadioSelect())

    bio = forms.CharField(label=mark_safe_lazy(
        _('Short biographical note in Polish (max. 500 characters, not required)')),
                          widget=forms.Textarea, max_length=500, required=False)
    bio_en = forms.CharField(label=_('Short biographical note in English (max. 500 characters)'), widget=forms.Textarea,
                             max_length=500)
    photo = forms.FileField(label=_('Photo'), required=False)
    phone = forms.CharField(label=_('Phone number'), max_length=64,
                            required=False,
                            help_text=_('(used only for organizational purposes)'))

    presentation_title = forms.CharField(
        label=mark_safe_lazy(_('Presentation title in Polish (not required)')),
        max_length=256, required=False)
    presentation_title_en = forms.CharField(
        label=_('Presentation title in English'), max_length=256)
    presentation_summary = forms.CharField(label=_('Presentation summary (max. 1800 characters)'),
                                           widget=forms.Textarea, max_length=1800)

    # presentation_post_conference_publication = forms.BooleanField(
    #     label=_('I am interested in including my paper in the post-conference publication'),
    #     required=False
    # )

    agree_data = None

    agree_terms = forms.BooleanField(
        label=mark_safe_lazy(
            _(u'I accept <a href="/en/info/terms-and-conditions/">CopyCamp Terms and Conditions</a>.'))
    )

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
            'presentation_thematic_track',
            # 'presentation_post_conference_publication',

            'agree_mailing',
            # 'agree_data',
            'agree_license',
            'agree_terms',
        ]


class RemindForm(ContactForm):
    form_tag = 'remind-me'
    save_as_tag = 'remind-me-2018'
    form_title = u'CopyCamp 2018'
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
