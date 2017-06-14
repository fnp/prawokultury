from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.core.mail import send_mail, mail_managers
from django.core.validators import validate_email
from django import forms
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from .models import Attachment, Contact


contact_forms = {}
admin_list_width = 0
class ContactFormMeta(forms.Form.__class__):
    def __new__(cls, *args, **kwargs):
        global admin_list_width
        model = super(ContactFormMeta, cls).__new__(cls, *args, **kwargs)
        assert model.form_tag not in contact_forms, 'Duplicate form_tag.'
        if model.admin_list:
            admin_list_width = max(admin_list_width, len(model.admin_list))
        contact_forms[model.form_tag] = model
        return model


class ContactForm(forms.Form):
    """Subclass and define some fields."""
    __metaclass__ = ContactFormMeta

    started = False
    form_tag = None
    save_as_tag = None
    form_title = _('Contact form')
    submit_label = _('Submit')
    admin_list = None
    notify_on_register = True
    notify_user = True

    required_css_class = 'required'
    contact = forms.EmailField(label=_('E-mail'), max_length=128)

    def __init__(self, *args, **kwargs):
        key = kwargs.pop('key', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        self.key = key

    def save(self, request):
        key = self.key
        body = {}
        for name, value in self.cleaned_data.items():
            if not isinstance(value, UploadedFile) and name != 'contact' and not name.startswith('_'):
                    body[name] = value
        save_as_tag = self.save_as_tag or self.form_tag
        if key:
            contact = Contact.objects.get(form_tag=save_as_tag, key=key)
            contact.body = body
            contact.ip = request.META['REMOTE_ADDR'] or '127.0.0.1'
            contact.contact = self.cleaned_data['contact']
            contact.save()
        else:
            contact = Contact.objects.create(body=body,
                    ip=request.META['REMOTE_ADDR'],
                    contact=self.cleaned_data['contact'],
                    form_tag=save_as_tag)
        for name, value in self.cleaned_data.items():
            if isinstance(value, UploadedFile):
                contact.attachment_set.filter(tag=name).delete()
                attachment = Attachment(contact=contact, tag=name)
                attachment.file.save(value.name, value)
                attachment.save()

        site = Site.objects.get_current()
        dictionary = {
            'form_tag': self.form_tag,
            'site_name': site.name,
            'site_domain': site.domain,
            'contact': contact,
            'form': self,
        }
        context = RequestContext(request)
        if self.notify_on_register:
            mail_managers_subject = render_to_string([
                    'contact/%s/mail_managers_subject.txt' % self.form_tag,
                    'contact/mail_managers_subject.txt',
                ], dictionary, context).strip()
            mail_managers_body = render_to_string([
                    'contact/%s/mail_managers_body.txt' % self.form_tag,
                    'contact/mail_managers_body.txt',
                ], dictionary, context)
            mail_managers(mail_managers_subject, mail_managers_body, fail_silently=True)

        try:
            validate_email(contact.contact)
        except ValidationError:
            pass
        else:
            if self.notify_user:
                mail_subject = render_to_string([
                        'contact/%s/mail_subject.txt' % self.form_tag,
                        'contact/mail_subject.txt',
                    ], dictionary, context).strip()
                mail_body = render_to_string([
                        'contact/%s/mail_body.txt' % self.form_tag,
                        'contact/mail_body.txt',
                    ], dictionary, context)
                send_mail(mail_subject, mail_body,
                    'no-reply@%s' % site.domain,
                    [contact.contact],
                    fail_silently=True)

        return contact
