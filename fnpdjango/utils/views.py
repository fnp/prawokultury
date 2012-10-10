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


def set_current_object(request, obj, in_url=True):
    request.CURRENT_OBJECT = obj
    request.CURRENT_OBJECT_IN_URL = in_url


def get_current_object(request, for_url=False):
    if for_url and not getattr(request, 'CURRENT_OBJECT_IN_URL', True):
        return None
    return getattr(request, 'CURRENT_OBJECT', None)
