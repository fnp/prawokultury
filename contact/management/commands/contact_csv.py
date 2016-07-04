# -*- coding: utf-8 -*-

from optparse import make_option
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-e', '--exclude-fields', dest='exclude', metavar='name,...', default='',
            help='Exclude specific body fields by name'),
        make_option('-m', '--mailto', dest='mailto', metavar='email,...', default='',
            help='Send by mail'),
    )
    help = 'Dump form entries in a csv file.'
    def handle(self, *args, **kwargs):
        from csv import writer
        from sys import stdout
        from django.conf import settings
        from django.core.mail import EmailMessage
        from contact.models import Contact
        from StringIO import StringIO

        excludes = set(kwargs['exclude'].split(','))

        buffer = StringIO()
        w = writer(buffer)

        lines = []
        headers = set()
        for c in Contact.objects.filter(form_tag__in=args):
            headers |= set(c.body.keys())
            lines.append(c)
        headers = sorted(headers - excludes)
        w.writerow([u'email'] + headers)
        for c in lines:
            row = [c.contact.encode('utf-8')]
            for h in headers:
                v = c.body.get(h)
                if isinstance(v, unicode):
                    v = v.encode('utf-8') 
                row.append(v)
            w.writerow(row)

        mailto = kwargs['mailto']
        if mailto:
            mailto = mailto.split(',')
            message = EmailMessage('Contacts CSV', 'Contacts CSV', settings.CONTACT_EMAIL, mailto)
            message.attach('contacts.csv', buffer.getvalue(), 'text/csv')
            message.send()
        else:
            print buffer.getvalue()

