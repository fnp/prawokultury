from fnpdjango.utils.text.textilepl import textile_pl

COMMENTS_APP = "django_comments_xtd"
COMMENTS_XTD_CONFIRM_EMAIL = False

MARKUP_FIELD_TYPES = (
    ('textile_pl', textile_pl),
)
COMMENTS_XTD_LIST_URL_ACTIVE = True
#COMMENTS_XTD_LIST_PAGINATE_BY = 10

THUMBNAIL_QUALITY = 95

GRAVATAR_DEFAULT_IMAGE = 'http://localhost:8000/static/img/avatar.png'

CAS_SERVER_URL = 'https://logowanie.nowoczesnapolska.org.pl/cas/'
CAS_VERSION = '3'


SPONSORS_THUMB_HEIGHT = None

PIWIK_URL = ''
PIWIK_SITE_ID = 0
