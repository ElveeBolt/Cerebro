from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Version


# Create your views here.
class VersionListView(LoginRequiredMixin, ListView):
    model = Version
    template_name = 'versions/index.html'
    context_object_name = 'versions'
    extra_context = {
        'title': 'История версий',
        'subtitle': 'Информация касательно выпусков и обновлений Cerebro',
    }
