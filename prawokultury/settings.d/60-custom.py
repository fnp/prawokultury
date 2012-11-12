from fnpdjango.utils.settings import LazyUGettextLazy as _
from migdal.helpers import EntryType

MIGDAL_TYPES = (
    EntryType('news', _('news'), commentable=True, on_main=True,
        promotable=True, categorized=True),
    EntryType('publications', _('publications')),
    EntryType('info', _('info')),
)

MENU_MODULE = 'prawokultury.menu_items'
