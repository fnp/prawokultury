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

CAS_SERVER_URL = 'http://logowanie.nowoczesnapolska.org.pl/cas/'
CAS_VERSION = '3'

HONEYPOT_FIELD_NAME='miut'

TAGGIT_AUTOSUGGEST_MODEL = ('questions', 'Tag')

GETPAID_BACKENDS = (
    'getpaid.backends.payu',
)

PIWIK_URL = ''
PIWIK_SITE_ID = 0


BROKER_URL = 'django://'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

SOUTH_MIGRATION_MODULES = {
    'getpaid' : 'prawokultury.migrations.getpaid',
    'payu': 'prawokultury.migrations.getpaid_payu',
    'taggit': 'taggit.south_migrations',
}
