from django.core.management import setup_environ
from prawokultury import settings
import sys

if len(sys.argv) < 2:
	print "give me file name pls"
	sys.exit(-1)

setup_environ(settings)

from contact.models import *

export_info = [
	("Created", 'created_at'),
	("ip", 'ip'),
	("Contact", 'contact'),
	("Form", 'form_tag'),
	]

conts = Contact.objects.all().order_by("created_at")

import json

json_fields = tuple(conts[0].body.keys())

# The inverse of zip is zip
headers, fields = zip(*export_info)     
rows = [headers + json_fields]
for cont in conts:
	qs = Contact.objects.filter(pk=cont.id)    
	rows.append([unicode(v) for v in qs.values_list(*fields)[0]] + [unicode(qs[0].body.get(f, 'N/A')) for f in json_fields])

import csv
with open(sys.argv[1],'w') as ofile:
	o = csv.writer(ofile, dialect='excel')
	for row in rows:
		o.writerow([r.encode('utf-8') for r in row])



