from django.contrib import admin
from django.forms import ModelForm
from .models import Contact
from django.utils.translation import ugettext as _
from .forms import contact_forms, admin_list_width
from django.template import Template
from django.utils.safestring import mark_safe
from django.conf.urls import patterns, url
from django.http import HttpResponse, Http404

from .utils import deunicode
from StringIO import StringIO
from csv import writer


class ContactAdminMeta(admin.ModelAdmin.__class__):
    def __getattr__(cls, name):
        if name.startswith('admin_list_'):
            return lambda self: ""
        raise AttributeError, name


class ContactAdmin(admin.ModelAdmin):
    __metaclass__ = ContactAdminMeta
    date_hierarchy = 'created_at'
    list_display = ['created_at', 'contact', 'form_tag'] + \
        ["admin_list_%d" % i for i in range(admin_list_width)]
    fields = ['form_tag', 'created_at', 'contact', 'ip', 'key']
    readonly_fields = ['form_tag', 'created_at', 'contact', 'ip', 'key']
    list_filter = ['form_tag']

    def admin_list(self, obj, nr):
        try:
            field_name = contact_forms[obj.form_tag].admin_list[nr]
        except BaseException, e:
            return ''
        else:
            return obj.body.get(field_name, '')

    def __getattr__(self, name):
        if name.startswith('admin_list_'):
            nr = int(name[len('admin_list_'):])
            return lambda obj: self.admin_list(obj, nr)
        raise AttributeError, name

    def change_view(self, request, object_id, extra_context=None):
        if object_id:
            try:
                instance = Contact.objects.get(pk=object_id)
                assert isinstance(instance.body, dict)
            except (Contact.DoesNotExist, AssertionError):
                pass
            else:
                # Create readonly fields from the body JSON.
                body_fields = ['body__%s' % k for k in instance.body.keys()]
                attachments = list(instance.attachment_set.all())
                body_fields += ['body__%s' % a.tag for a in attachments]
                self.readonly_fields.extend(body_fields)

                # Find the original form.
                try:
                    orig_fields = contact_forms[instance.form_tag]().fields
                except KeyError:
                    orig_fields = {}

                # Try to preserve the original order.
                admin_fields = []
                orig_keys = list(orig_fields.keys())
                while orig_keys:
                    key = orig_keys.pop(0)
                    key = "body__%s" % key
                    if key in body_fields:
                        admin_fields.append(key)
                        body_fields.remove(key)
                admin_fields.extend(body_fields)

                self.fieldsets = [
                    (None, {'fields': self.fields}),
                    (_('Body'), {'fields': admin_fields}),
                ]

                # Create field getters for fields and attachments.
                for k, v in instance.body.items():
                    f = (lambda v: lambda self: v)(v)
                    f.short_description = orig_fields[k].label if k in orig_fields else _(k)
                    setattr(self, "body__%s" % k, f)

                download_link = "<a href='%(url)s'>%(url)s</a>"
                for attachment in attachments:
                    k = attachment.tag
                    link = mark_safe(download_link % {
                            'url': attachment.get_absolute_url()})
                    f = (lambda v: lambda self: v)(link)
                    f.short_description = orig_fields[k].label if k in orig_fields else _(k)
                    setattr(self, "body__%s" % k, f)
        return super(ContactAdmin, self).change_view(request, object_id,
            extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        context = dict()
        if 'form_tag' in request.GET:
            form = contact_forms.get(request.GET['form_tag'])
            context['extract_types'] = [dict(slug = 'all', label = _('all'))] + [dict(slug = 'contacts', label = _('contacts'))]
            context['extract_types'] += [type for type in getattr(form, 'extract_types', [])]
        return super(ContactAdmin, self).changelist_view(request, extra_context = context)

    def get_urls(self):
        urls = super(ContactAdmin, self).get_urls()
        return patterns('',
            url(r'^extract/(?P<form_tag>[\w-]+)/(?P<extract_type_slug>[\w-]+)/$', self.admin_site.admin_view(extract_view), name='contact_extract')
        ) + super(ContactAdmin, self).get_urls()


def extract_view(request, form_tag, extract_type_slug):
    retval = StringIO()
    toret = writer(retval)
    contacts_by_spec = dict()
    try:
        form = [f for f in contact_forms.values() if f.save_as_tag == form_tag][0]
    except IndexError:
        form = None
    if form is None and extract_type_slug not in ('contacts', 'all'):
        raise Http404

    q = Contact.objects.filter(form_tag = form_tag)
    at_year = request.GET.get('created_at__year')
    at_month = request.GET.get('created_at__month')
    if at_year:
        q = q.filter(created_at__year = at_year)
        if at_month:
            q = q.filter(created_at__month = at_month)

    if extract_type_slug == 'contacts':
        keys = set(['contact'])
    else:
        keys = set(['contact', 'ip', 'created_at'])
        for contact in q.all():
            if extract_type_slug == 'all':
                keys.update(contact.body.keys())
            else:
                keys.update(form.get_extract_fields(contact, extract_type_slug))
    
    keys = sorted(keys)
    key_labels = {f.name: f.verbose_name.encode('utf-8') for f in Contact._meta.fields}
    if form is not None:
        fi = form()
        key_labels.update({k: v.label.encode('utf-8') for (k, v) in fi.fields.items()})
        
    toret.writerow([key_labels.get(key, key) for key in keys])
    for contact in q.all():
            if extract_type_slug == 'contacts':
                records = [dict(contact=contact.contact)]
            elif extract_type_slug == 'all':
                records = [dict(contact = contact.contact, ip=contact.ip, created_at=contact.created_at, **contact.body)]
            else:
                records = form.get_extract_records(keys, contact, extract_type_slug)

            for record in records:
                toret.writerow([deunicode(record.get(key, '-')) for key in keys])

    response = HttpResponse(retval.getvalue(), content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % form_tag
    return response

admin.site.register(Contact, ContactAdmin)
