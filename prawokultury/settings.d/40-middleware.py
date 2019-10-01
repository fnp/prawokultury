MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'fnpdjango.middleware.URLLocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'prawokultury.middleware.ExemptableHoneypotViewMiddleware',
    'honeypot.middleware.HoneypotResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django_cas_ng.middleware.CASMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'fnp_django_pagination.middleware.PaginationMiddleware',
    'fnpdjango.middleware.SetRemoteAddrFromXRealIP',
)


