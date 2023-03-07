from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import HelpCategory


# Create your views here.
class HelpListView(LoginRequiredMixin, ListView):
    model = HelpCategory
    template_name = 'help/index.html'
    context_object_name = 'categories'
    extra_context = {
        'title': 'Помощь',
        'subtitle': 'Страница ответов на часто задаваемые вопросы'
    }
