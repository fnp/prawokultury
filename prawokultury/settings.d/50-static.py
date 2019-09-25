MEDIA_ROOT = path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'fnpdjango.pipeline_storage.GzipPipelineCachedStorage'

PIPELINE = {
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    'STYLESHEETS': {
        'base': {
            'source_filenames': (
                'css/base.scss',
                'css/layout.scss',
                'css/header.scss',
                'css/menu.scss',
                'css/search.scss',
                'css/sidebar.scss',
                'css/promobox.scss',
                'css/entry.scss',
                'css/footer.scss',
                'css/prevnext.scss',
                'css/forms.scss',
                'events/events.scss',

                'contrib/lightbox/css/lightbox.css',
            ),
            'output_filename': 'compressed/base.css',
        },
    },
    'JAVASCRIPT': {
        'base': {
            'source_filenames': (
                'js/promobox.js',
                'js/workshop_form.js',
                'js/optional_fields.js',
                'contrib/lightbox/js/lightbox.min.js',
            ),
            'output_filename': 'compressed/base.js',
        },
    },
    'COMPILERS': (
        'pipeline.compilers.sass.SASSCompiler',
    ),
}
