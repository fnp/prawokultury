from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from fnpdjango.utils.views import serve_file
from .forms import contact_forms
from .models import Attachment


def form(request, form_tag):
    try:
        form_class = contact_forms[form_tag]
    except KeyError:
        raise Http404
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return redirect('contact_thanks', form_tag)
    else:
        form = form_class()
    return render(request,
                ['contact/%s/form.html' % form_tag, 'contact/form.html'],
                {'form': form}
            )


def thanks(request, form_tag):
    if form_tag not in contact_forms:
        raise Http404

    return render(request,
                ['contact/%s/thanks.html' % form_tag, 'contact/thanks.html']
            )


@permission_required('contact.change_attachment')
def attachment(request, contact_id, tag):
    attachment = get_object_or_404(Attachment, contact_id=contact_id, tag=tag)
    return serve_file(attachment.file.url)
