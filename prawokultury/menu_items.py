from migdal.models import Entry
from menu.helpers import ObjectMenuItem, MenuItem
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


ITEMS = []

def add_entry(**qs):
    try:
        entry = Entry.objects.get(**qs)
    except Entry.DoesNotExist:
        return
    if not entry.published:
        return
    ITEMS.append(ObjectMenuItem(entry))

add_entry(slug_pl='co')
add_entry(slug_pl='gdzie')
add_entry(slug_pl='program')
add_entry(slug_pl='media')
ITEMS.append(MenuItem(reverse_lazy('contact_form', args=['register']), _('Form')))
add_entry(slug_pl='materialy')
add_entry(slug_pl='kontakt')
