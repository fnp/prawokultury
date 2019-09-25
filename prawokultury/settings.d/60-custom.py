from migdal.helpers import EntryType

MIGDAL_TYPES = (
    EntryType('info', 'info', commentable=False, on_main=False),
)

MIGDAL_TAXONOMIES = ()
MIGDAL_MAIN_PAGE_ENTRY = {'slug_pl': 'co'}

CONTACT_FORMS_MODULE = 'prawokultury.contact_forms'

MENU_MODULE = 'prawokultury.menu_items'

# Use Nginx's X-accel when serving files with helpers.serve_file().
# See http://wiki.nginx.org/X-accel
X_ACCEL_REDIRECT = False

REGISTRATION_LIMIT = 100
