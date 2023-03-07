from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Database, Post
from api import api


# Create your views here.
class DatabaseListView(LoginRequiredMixin, ListView):
    model = Database
    template_name = 'databases/index.html'
    context_object_name = 'databases'
    extra_context = {
        'title': 'Источники данных',
        'subtitle': 'Список источников данных среди которых осуществляется поиск'
    }


class DatabaseView(LoginRequiredMixin, DetailView):
    model = Database
    template_name = 'databases/database.html'
    extra_context = {
        'title': 'Источник данных',
        'subtitle': 'Детальная информация об источнике данных'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index_info'] = api.get_index_info(index=self.object.index)
        return context


class PostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'databases/post.html'
    extra_context = {
        'title': 'Источник данных',
        'subtitle': 'Детальная информация об источнике данных',
    }
