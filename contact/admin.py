from django.contrib import admin
from django.forms import ModelForm
from .models import Contact
from django.utils.translation import ugettext as _
from .forms import contact_forms, admin_list_width
from django.template import Template
from django.utils.safestring import mark_safe


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
    fields = ['form_tag', 'created_at', 'contact', 'ip']
    readonly_fields = ['form_tag', 'created_at', 'contact', 'ip']
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


admin.site.register(Contact, ContactAdmin)
