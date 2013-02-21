HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/prawokultury'
    },
}

HAYSTACK_DOCUMENT_FIELD = "text"
