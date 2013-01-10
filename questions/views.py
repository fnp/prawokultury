from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from .forms import QuestionForm


class QuestionFormView(FormView):
    form_class = QuestionForm
    template_name = "questions/question_form.html"
    success_url = reverse_lazy("questions_thanks")

    def form_valid(self, form):
        form.save()
        return super(QuestionFormView, self).form_valid(form)
