# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django import forms
from django.core.mail import send_mail

from contact.forms import ContactForm
from contact.models import Contact
from contact.fields import HeaderField
from django.utils.functional import lazy
from django.utils.translation import ugettext_noop as _
from django.utils.safestring import mark_safe
from migdal.models import Entry

from prawokultury.countries import COUNTRIES, TRAVEL_GRANT_COUNTRIES

mark_safe_lazy = lazy(mark_safe, unicode)


class RegistrationForm(ContactForm):
    form_tag = 'register'

    save_as_tag = '2017'
    conference_name = u'CopyCamp 2017'
    notify_on_register = False
    
    form_title = _('Registration')
    admin_list = ['first_name', 'last_name', 'organization']

    travel_grant_countries = TRAVEL_GRANT_COUNTRIES

    first_name = forms.CharField(label=_('First name'), max_length=128)
    last_name = forms.CharField(label=_('Last name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'), max_length=256, required=False)
    country = forms.ChoiceField(label=_('Country of residence'), choices=zip(COUNTRIES, COUNTRIES))
    travel_grant = forms.BooleanField(
        label=_('I require financial assistance to attend CopyCamp 2017.'), required=False)
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
           ('only-28th', _('September 28th only')),
           ('only-29th', _('September 29th only')),
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
        label=_('I am interested in receiving information about the Modern Poland Foundation\'s activities by e-mail'),
        required=False
    )
    agree_data = forms.BooleanField(
        label=_('Permission for data processing'),
        help_text=_(u'I hereby grant Modern Poland Foundation (Fundacja Nowoczesna Polska, ul. Marszałkowska 84/92, 00-514 Warszawa) permission to process my personal data (name, e-mail address) for purposes of registration for CopyCamp conference.')
    )
    agree_license = forms.BooleanField(
        label=_('Permission for publication'),
        help_text=mark_safe_lazy(_(u'I agree to having materials, recorded during the conference, released under the terms of <a href="http://creativecommons.org/licenses/by-sa/3.0/deed">CC\u00a0BY-SA</a> license and to publishing my image.')),
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
        return [self[name] for name in ('agree_mailing', 'agree_data', 'agree_license', 'agree_toc')]


tracks = (
    (_('business models, heritage digitization, remix'),
     _('What are the boundaries of appropriation in culture? '
       'Who owns the past and whether these exclusive rights allow to '
       'control present and future? How to make money from creativity without selling yourself?')),
    (_('health, food, security, and exclusive rights'),
     _('Who owns medicines and equipment necessary to provide health care? '
       'Who owns grain and machines used to harvest it? '
       'To what extent exclusive rights can affect what you eat, '
       'how you exercise, whether you can apply a specific treatment?')),
    (_('text and data mining, machine learning, online education'),
     _('Do you think own the data you feed to algorithms? Or maybe you think you own these algorithms? '
       'What if you can’t mine the data because you actually don’t own any of those rights? '
       'What does it mean to own data about someone, or data necessary for that person’s education?')),
    (_('IoT: autonomous cars, smart homes, wearables'),
     _('What does it mean to own exclusive rights to software and data used to construct autonomous agents? '
       'What will it mean in a near future?')),
    (_('hacking government data, public procurement, public aid in culture'),
     _('Who owns information created using public money? How can this information be appropriated? '
       'What is the role of government in the development of information infrastructure?')),
)


class RegisterSpeaker(RegistrationForm):
    form_tag = 'register-speaker'
    save_as_tag = '2017-speaker'
    form_title = _('Open call for presentations')
    notify_on_register = False

    # inherited fields included so they are not translated
    first_name = forms.CharField(label=_('First name'), max_length=128)
    last_name = forms.CharField(label=_('Last name'), max_length=128)
    organization = forms.CharField(label=_('Organization'),
            max_length=256, required=False)
    agree_mailing = forms.BooleanField(
        label=_('I am interested in receiving information about the Modern Poland Foundation\'s activities by e-mail'),
        required=False
    )
    agree_license = forms.BooleanField(
        label=_('Permission for publication'),
        help_text=mark_safe_lazy(_(u'I agree to having materials, recorded during the conference, released under the terms of <a href="http://creativecommons.org/licenses/by-sa/3.0/deed">CC\u00a0BY-SA</a> license and to publishing my image.')),
        required=False
    )

    presentation_thematic_track = forms.ChoiceField(
        label=_('Please select one thematic track'),
        choices=[(t, mark_safe('<strong>%s</strong><p style="margin-left: 20px;">%s</p>' % (t, desc))) for t, desc in tracks],
        widget=forms.RadioSelect())

    bio = forms.CharField(label=_('Short biographical note in English (max. 500 characters)'), widget=forms.Textarea,
                          max_length=500, required=False)
    photo = forms.FileField(label=_('Photo'), required=False)
    phone = forms.CharField(label=_('Phone number'), max_length=64,
                            required=False,
                            help_text=_('Used only for organizational purposes.'))

    presentation_title = forms.CharField(
        label=mark_safe_lazy(_('Title of the presentation in English')),
        max_length=256, required=False)
    presentation_summary = forms.CharField(label=_('Summary of presentation (max. 1800 characters)'),
                                           widget=forms.Textarea, max_length=1800)

    # presentation_post_conference_publication = forms.BooleanField(
    #     label=_('I am interested in including my paper in the post-conference publication'),
    #     required=False
    # )

    agree_data = None

    agree_terms = forms.BooleanField(
        label=mark_safe_lazy(_(u'I accept <a href="/en/info/terms-and-conditions/">'
                               u'CopyCamp Terms and Conditions</a>.'))
    )

    # workshop = forms.BooleanField(label=_('Workshop'), required=False)
    # workshop_title = forms.CharField(label=_('Title of workshop'),
    #        max_length=256, required=False)
    # workshop_summary = forms.CharField(label=_('Summary of workshop (max. 1800 characters)'),
    #        widget=forms.Textarea, max_length=1800, required=False)

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
            'photo',
            'presentation_title',
            'presentation_summary',
            'presentation_thematic_track',
            # 'presentation_post_conference_publication',
            # 'workshop',
            # 'workshop_title',
            # 'workshop_summary',

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


def workshop_field(label):
    return forms.BooleanField(label=_(label), required=False)


class WorkshopForm(ContactForm):
    form_tag = 'workshops'
    save_as_tag = 'workshops-2017'
    conference_name = u'CopyCamp 2017'
    form_title = _('Workshop')
    notify_on_register = False

    first_name = forms.CharField(label=_('First name'), max_length=128)
    last_name = forms.CharField(label=_('Last name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'), max_length=256, required=False)
    country = forms.CharField(label=_('Country'), max_length=128)

    _header = HeaderField(
        label=mark_safe_lazy(_("<h3>I'll take a part in workshops</h3>")),
        help_text=_('Only workshops with any spots left are visible here.'))

    _h1 = HeaderField(label=mark_safe_lazy(_("<strong>Thursday, September 28th, 10 a.m.–12 noon</strong>")))

    w_mileszyk = workshop_field(
        u'Natalia Mileszyk, Dimitar Dimitrov, Diego Naranjo: School of Rock(ing) Copyright: United to #fixcopyright')
    w_wang = workshop_field(
        u'Jacob Riddersholm Wang, Pernille Feldt, Martin Appelt: Heritage gone digital - beyond legal rights')

    _h2 = HeaderField(label=mark_safe_lazy(_("<strong>Thursday, September 28th, 12 noon–2 p.m.</strong>")))

    w_vanderwaal = workshop_field(u'Sander van der Waal, Danny Lämmerhirt: Tackling open license proliferation')

    _h2a = HeaderField(label=mark_safe_lazy(_("<strong>Friday, September 29th, 9 a.m.–11 noon</strong>")))

    w_nobre = workshop_field(u'Teresa Nobre, Paul Keller, Sean Flynn: Researching the Impact of Copyright User Rights')
    w_nobre_question = forms.CharField(
        label=mark_safe_lazy(_(
            u'Please describe the most important recent changes to copyright user rights in your national law. '
            u'(max 1500 characters)')),
        max_length=1500, widget=forms.Textarea, required=False)

    _h3 = HeaderField(label=mark_safe_lazy(_("<strong>Friday, September 29th, 10 a.m.–12 noon</strong>")))

    w_youtube = workshop_field(
        u'Kiki Ganzemüller: YouTube Songwriter Workshop: Rights Management & Building a Presence on YouTube')

    _h4 = HeaderField(label=mark_safe_lazy(_("<strong>Friday, September 29th, 12 noon–2 p.m.</strong>")))

    w_murray = workshop_field(
        u'Peter Murray-Rust: Wikidata, ContentMine and the automatic liberation of factual data: '
        u'(The Right to Read is the Right To Mine)')  # 30

    w_zimmermann = workshop_field(u'Jeremie Zimmermann: Hackers ethics and peer-to-peer philosophy in care')

    _header_1 = HeaderField(label='')
    _header_2 = HeaderField(label='')

    start_workshops = ('mileszyk', 'wang', 'vanderwaal', 'nobre', 'youtube', 'murray', 'zimmermann')

    slots = (
        ('_h1', 'mileszyk', 'wang'),
        ('_h2', 'vanderwaal'),
        ('_h2a', 'nobre', '_h3', 'youtube'),
        ('_h4', 'murray', 'zimmermann'),
    )

    limits = {
        'mileszyk': 25,
        'wang': 25,
        'vanderwaal': 25,
        'nobre': 25,
        'youtube': 40,
        'murray': 35,
        'zimmermann': 35,
    }

    agree_mailing = forms.BooleanField(
        label=_('I am interested in receiving information about the Modern Poland Foundation\'s activities by e-mail'),
        required=False)
    agree_data = forms.BooleanField(
        label=_('Permission for data processing'),
        help_text=_(
            u'I hereby grant Modern Poland Foundation (Fundacja Nowoczesna Polska, ul. Marszałkowska 84/92, '
            u'00-514 Warszawa) permission to process my personal data (name, e-mail address) for purposes of '
            u'registration for CopyCamp conference.'))
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
                    if workshop == 'youtube' and counts[workshop] == 30:
                        send_mail(u'Warsztaty YouTube', u'Przekroczono limit 30 osób na warsztaty YouTube',
                                  'no-reply@copycamp.pl',
                                  ['krzysztof.siewicz@nowoczesnapolska.org.pl'],
                                  fail_silently=True)

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
