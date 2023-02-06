from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Database
from api import api


# Create your views here.
@login_required(redirect_field_name=None)
def index(request):
    databases = Database.objects.all()

    context = {
        'title': 'Источники данных',
        'subtitle': 'Список источников данных среди которых осуществляется поиск',
        'databases': databases
    }
    return render(request, 'databases/index.html', context=context)


@login_required(redirect_field_name=None)
def database(request, index):
    database = Database.objects.filter(index=index).get()
    index_info = api.get_index_info(index=database.index)

    context = {
        'title': 'Источник данных',
        'subtitle': 'Детальная информация об источнике данных',
        'database': database,
        'index_info': index_info[0]
    }

    return render(request, 'databases/database.html', context=context)