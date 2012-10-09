"""
View-specific utilities.
"""

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect


def serve_file(url):
    """Serves an URL either though Nginx's X-accel, or by redirection.""" 
    if settings.X_ACCEL_REDIRECT:
        response = HttpResponse()
        response['Content-Type'] = ""
        response['X-Accel-Redirect'] = url
        return response
    else:
        return HttpResponseRedirect(url)
