MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'fnpdjango.middleware.URLLocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'prawokultury.middleware.ExemptableHoneypotViewMiddleware',
    'honeypot.middleware.HoneypotResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

if 'django_cas' in INSTALLED_APPS:
    MIDDLEWARE_CLASSES += (
        'django_cas.middleware.CASMiddleware',
    )

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
    'piwik.django.middleware.PiwikMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'fnpdjango.middleware.SetRemoteAddrFromXRealIP',
)


