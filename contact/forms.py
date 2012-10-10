from django.contrib.sites.models import Site
from django.core.files.uploadedfile import UploadedFile
from django.core.mail import send_mail, mail_managers
from django.core.validators import email_re
from django import forms
from django.template.loader import render_to_string
from django.template import RequestContext
from .models import Attachment, Contact


contact_forms = {}
class ContactFormMeta(forms.Form.__metaclass__):
    def __new__(cls, *args, **kwargs):
        model = super(ContactFormMeta, cls).__new__(cls, *args, **kwargs)
        assert model.form_tag not in contact_forms, 'Duplicate form_tag.'
        contact_forms[model.form_tag] = model
        return model


class ContactForm(forms.Form):
    """Subclass and define some fields."""
    __metaclass__ = ContactFormMeta
    required_css_class = 'required'
    contact = forms.CharField(max_length=128)
    form_tag = None

    def save(self, request):
        body = {}
        for name, value in self.cleaned_data.items():
            if not isinstance(value, UploadedFile) and name != 'contact':
                    body[name] = value
        contact = Contact.objects.create(body=body,
                    ip=request.META['REMOTE_ADDR'],
                    contact=self.cleaned_data['contact'],
                    form_tag=self.form_tag)
        for name, value in self.cleaned_data.items():
            if isinstance(value, UploadedFile):
                attachment = Attachment(contact=contact, tag=name)
                attachment.file.save(value.name, value)
                attachment.save()

        site = Site.objects.get_current()
        dictionary = {
            'form_tag': self.form_tag,
            'site_name': site.name,
            'site_domain': site.domain,
            'contact': contact,
        }
        context = RequestContext(request)
        mail_managers_subject = render_to_string([
                'contact/%s/mail_managers_subject.txt' % self.form_tag,
                'contact/mail_managers_subject.txt', 
            ], dictionary, context)
        mail_managers_body = render_to_string([
                'contact/%s/mail_managers_body.txt' % self.form_tag,
                'contact/mail_managers_body.txt', 
            ], dictionary, context)
        mail_managers(mail_managers_subject, mail_managers_body, 
            fail_silently=True)

        if email_re.match(contact.contact):
            mail_subject = render_to_string([
                    'contact/%s/mail_subject.txt' % self.form_tag,
                    'contact/mail_subject.txt', 
                ], dictionary, context)
            mail_body = render_to_string([
                    'contact/%s/mail_body.txt' % self.form_tag,
                    'contact/mail_body.txt', 
                ], dictionary, context)
            send_mail(mail_subject, mail_body,
                'no-reply@%s' % site.domain,
                [contact.contact],
                fail_silently=True)

        return contact
