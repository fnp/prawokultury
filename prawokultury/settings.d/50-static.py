MEDIA_ROOT = path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'fnpdjango.pipeline_storage.GzipPipelineCachedStorage'

PIPELINE = {
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    'COMPILERS': [
        'pipeline.compilers.sass.SASSCompiler',
    ],
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
                'fnpdjango/annoy/annoy.css',
            ),
            'output_filename': 'compressed/base.css',
        },
        'questions': {
            'source_filenames': (
                'questions/tagcloud.scss',
            ),
            'output_filename': 'compressed/questions.css'
        }
    },
    'JAVASCRIPT': {
        'base': {
            'source_filenames': (
                'js/promobox.js',
                'shop/shop.js',
                'fnpdjango/annoy/annoy.js',
            ),
            'output_filename': 'compressed/base.js',
        },
        'questions': {
            'source_filenames': (
                'questions/tagcloud.js',
            ),
            'output_filename': 'compressed/questions.js'
        }
    }
}
