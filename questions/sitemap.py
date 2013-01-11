from django.contrib.sitemaps import Sitemap
from .models import Question

class QuestionSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Question.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.changed_at

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    "question": QuestionSitemap,
}
