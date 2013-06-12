MEDIA_ROOT = path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
PIPELINE_CSS = {
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

        ),
        'output_filename': 'compressed/base.css',
    },
    'questions': {
        'source_filenames': (
            'questions/tagcloud.scss',
        ),
        'output_filename': 'compressed/questions.css'
    }
}
PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'js/promobox.js',

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

PIPELINE_COMPILERS = (
  'pipeline.compilers.sass.SASSCompiler',
)

PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'
