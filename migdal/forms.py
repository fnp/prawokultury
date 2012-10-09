# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django import forms
from django.utils.translation import ugettext_lazy as _, get_language
from migdal.models import Entry
from migdal import app_settings
from fnpdjango.utils.text import slughifi
from django.core.mail import mail_managers
from django import template


def get_submit_form(*args, **kwargs):
    lang = get_language()

    class SubmitForm(forms.ModelForm):
        class Meta:
            model = Entry
            fields = ['title_%s' % lang, 'lead_%s' % lang,
                'author', 'author_email', 'categories']
            required = ['title_%s' % lang]

        def __init__(self, *args, **kwargs):
            super(SubmitForm, self).__init__(*args, **kwargs)
            title = self.fields['title_%s' % lang]
            title.required = True
            title.label = _('Title')
            lead = self.fields['lead_%s' % lang]
            lead.required = True
            lead.label = _('Content')

        def clean(self):
            data = super(SubmitForm, self).clean()
            data['type'] = app_settings.TYPE_SUBMIT
            orig_slug = slughifi(data.get('title_%s' % lang, ''))
            slug = orig_slug
            number = 2
            while Entry.objects.filter(**{'slug_%s' % lang: slug}).exists():
                slug = "%s-%s" % (orig_slug, number)
                number += 1
            data['slug_%s' % lang] = slug
            self.cleaned_data = data
            return data

        def save(self, *args, **kwargs):
            entry = super(SubmitForm, self).save(commit=False)
            # Something's wrong with markup fields, they choke on None here.
            for f in 'lead_en', 'lead_pl', 'body_en', 'body_pl':
                if getattr(entry, f) is None:
                    setattr(entry, f, '')
            for f in 'slug_%s' % lang, 'type':
                setattr(entry, f, self.cleaned_data[f])
            entry.save()
            entry = super(SubmitForm, self).save(*args, **kwargs)
            mail_managers(u"Nowy wpis",
                template.loader.get_template(
                    'migdal/mail/manager_new_entry.txt').render(
                        template.Context({'object': entry})))

    return SubmitForm(*args, **kwargs)