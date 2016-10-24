# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django import forms
from contact.forms import ContactForm
from contact.models import Contact
from contact.fields import HeaderField
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from migdal.models import Entry

mark_safe_lazy = lazy(mark_safe, unicode)


class RegistrationForm(ContactForm):
    form_tag = 'register'

    save_as_tag = '2016'
    conference_name = u'CopyCamp 2016'
    
    form_title = _('Registration')
    admin_list = ['first_name', 'last_name', 'organization']

    first_name = forms.CharField(label=_('First name'), max_length=128)
    last_name = forms.CharField(label=_('Last name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'), 
            max_length=256, required=False)
    country = forms.CharField(label=_('Country'), max_length=128)

    days = forms.ChoiceField(
       label=_("I'm planning to show up on"),
       choices=[
           ('both', _('Both days of the conference')),
           ('only-27th', _('October 27th only')),
           ('only-28th', _('October 28th only')),
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
    distance = forms.ChoiceField(
        required=False,
        label=_("3. How far will you travel to attend CopyCamp?"),
        choices=[
            ('0-50', _('0-50 km')),
            ('51-100', _('51-100 km')),
            ('101-200', _('101-200 km')),
            ('200+', _('200 km or more')),
        ], widget=forms.RadioSelect())
    areas = forms.MultipleChoiceField(
        required=False,
        label=_("4. Please indicate up to 3 areas you feel most affiliated with"),
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
        label=_("5. Please indicate how you received information about the conference:"),
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
            ('idea', _('the main idea of the conference')),
            ('speaker', _('particular speaker(s)')),
            ('networking', _('good networking occasion')),
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

    def main_fields(self):
        return [self[name] for name in ('first_name', 'last_name', 'contact', 'organization', 'country', 'days')]

    def survey_fields(self):
        return [self[name] for name in (
            'times_attended', 'age', 'distance',
            'areas', 'areas_other', 'source', 'source_other', 'motivation', 'motivation_other')]

    def agreement_fields(self):
        return [self[name] for name in ('agree_mailing', 'agree_data', 'agree_license', 'agree_toc')]


tracks = (
    _('Copyright and Art'),
    _('Remuneration Models'),
    _('Copyright, Education and Science'),
    _('Technology, Innovation and Copyright'),
    _('Copyright and Human Rights'),
    _('Copyright Enforcement'),
    _('Copyright Debate'),
    _('Copyright Lawmaking'),
)


class RegisterSpeaker(RegistrationForm):
    form_tag = 'register-speaker'
    save_as_tag = '2016-speaker'
    form_title = _('Open call for presentations')

    presentation_thematic_track = forms.ChoiceField(
        label=_('Please select one thematic track'),
        choices=[(t, t) for t in tracks], widget=forms.RadioSelect())

    bio = forms.CharField(label=mark_safe_lazy(
        _('Short biographical note in Polish (max. 500 characters, fill <strong>at least</strong> one bio)')),
                          widget=forms.Textarea, max_length=500, required=False)
    bio_en = forms.CharField(label=_('Short biographical note in English (max. 500 characters)'), widget=forms.Textarea,
                             max_length=500, required=False)
    photo = forms.FileField(label=_('Photo'), required=False)
    phone = forms.CharField(label=_('Phone number'), max_length=64,
                            required=False,
                            help_text=_('Used only for organizational purposes.'))

    # presentation = forms.BooleanField(label=_('Presentation'), required=False)
    presentation_title = forms.CharField(
        label=mark_safe_lazy(_('Title of the presentation in Polish (fill <strong>at least</strong> one title)')),
        max_length=256, required=False)
    presentation_title_en = forms.CharField(label=_('Title of the presentation in English'),
                                            max_length=256, required=False)
    # presentation = forms.FileField(label=_('Presentation'), required=False)
    presentation_summary = forms.CharField(label=_('Summary of presentation (max. 1800 characters)'),
                                           widget=forms.Textarea, max_length=1800)

    presentation_post_conference_publication = forms.BooleanField(
        label=_('I am interested in including my paper in the post-conference publication'),
        required=False
    )

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
            'bio_en',
            'photo',
            # 'presentation',
            'presentation_title',
            'presentation_title_en',
            'presentation_summary',
            'presentation_thematic_track',
            'presentation_post_conference_publication',
            # 'workshop',
            # 'workshop_title',
            # 'workshop_summary',

            'agree_mailing',
            # 'agree_data',
            'agree_license',
            'agree_terms',
        ]

    def clean(self):
        cleaned_data = super(RegisterSpeaker, self).clean()
        errors = []
        if not cleaned_data.get('bio') and not cleaned_data.get('bio_en'):
            errors.append(forms.ValidationError(_('Fill at least one bio!')))
        if not cleaned_data.get('presentation_title') and not cleaned_data.get('presentation_title_en'):
            errors.append(forms.ValidationError(_('Fill at least one title!')))
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data


class NextForm(ContactForm):
    form_tag = '/next'
    form_title = _('Next CopyCamp')

    name = forms.CharField(label=_('Name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'),
                                   max_length=256, required=False)


class WorkshopForm(ContactForm):
    form_tag = 'workshops'
    save_as_tag = 'workshops-2016'
    conference_name = u'CopyCamp 2016'
    form_title = _('Workshop')

    name = forms.CharField(label=_('Name'), max_length=128)
    contact = forms.EmailField(label=_('E-mail'), max_length=128)
    organization = forms.CharField(label=_('Organization'),
                                   max_length=256, required=False)
    country = forms.CharField(label=_('Country'), max_length=128)

    _header = HeaderField(
        label=mark_safe_lazy(_("<h3>I'll take a part in workshops</h3>")),
        help_text=_('Only workshops with any spots left are visible here.'))

    _h1 = HeaderField(label=mark_safe_lazy(_("<strong>Thursday, October 27th, 10 a.m.–12 noon</strong>")))

    w_dimitrov = forms.BooleanField(label=_(u'Dimitar Dimitrov: Hacking Brussels'), required=False)
    w_vangompel = forms.BooleanField(label=_(
        u'Stef van Gompel: Methods and constraints for including evidence in IP lawmaking'), required=False)

    _h2 = HeaderField(label=mark_safe_lazy(_("<strong>Friday, October 28th, 10 a.m.–12 noon</strong>")))

    w_siewicz = forms.BooleanField(label=_(
        u'dr Krzysztof Siewicz, dr Marta Hoffman-Sommer: '
        u'Legal aspects of using research data in the age of Open Data'), required=False)
    w_siewicz_project = forms.CharField(
        label=mark_safe(
            u'<p style="margin-top: 0"><strong>Qualification for this workshop will be based on the answers '
            u'for the following problem:</strong></p>'
            u'Please choose a particular dataset from any research project you are involved in and provide '
            u'a description (no more than 1800 characters). Selected datasets will be discussed during '
            u'the workshop as case studies. In your description, please include the following information: '
            u'What is the research goal of the project (in the context of the chosen dataset)? '
            u'What data is being collected and how is it stored? What is the process of data collection '
            u'or generation? Who is involved in collecting or producing the data and in what manner?'),
        max_length=1800, widget=forms.Textarea, required=False)
    w_google = forms.BooleanField(label=_(
        u'Marcin Olender, Google: Prawo autorskie na YouTube (workshop in Polish)'), required=False)

    _h3 = HeaderField(label=mark_safe_lazy(_("<strong>Friday, October 28th, 12 noon–2 p.m.</strong>")))

    w_patronite = forms.BooleanField(label=_(
        u'Mateusz Górski, Michał Leksiński, Patronite: Jak zarabiać i się nie sprzedać – warsztaty dla twórców '
        u'(workshop in Polish)'),
        required=False)

    w_gurionova = forms.BooleanField(label=_(
        u'Olga Goriunova: The Lurker and the politics of knowledge in data culture'), required=False)

    _header_1 = HeaderField(label='')

    start_workshops = ('dimitrov', 'vangompel', 'siewicz', 'google', 'patronite')

    slots = (('_h1', 'dimitrov', 'vangompel'), ('_h2', 'siewicz', 'google'), ('_h3', 'patronite', 'gurionova'))

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
        # self.limit_reached = Contact.objects.filter(form_tag=self.save_as_tag).count() >= 60
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
                if contact.body.get('w_%s' % workshop, False): counts[workshop] += 1
        some_full = False
        for k, v in counts.items():
            if v >= 30:
                some_full = True
                if 'w_%s' % k in self.fields:
                    del self.fields['w_%s' % k]
                if k in self.workshops:
                    self.workshops.remove(k)
        if not some_full:
            self.fields['_header'].help_text = None

    def clean(self):
        if self.cleaned_data.get('w_siewicz') and not self.cleaned_data.get('w_siewicz_project'):
            self._errors['w_siewicz_project'] = [_("Please submit your answer to qualify for this workshop")]
        for slot in self.slots:
            if sum(1 for w in slot if self.cleaned_data.get('w_%s' % w)) > 1:
                self._errors[slot[0]] = [_("You can't choose more than one workshop during the same period")]
        if not any(self.cleaned_data.get('w_%s' % w) for w in self.start_workshops):
            self._errors['_header'] = [_("Please choose at least one workshop.")]
        return self.cleaned_data
