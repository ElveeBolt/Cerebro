from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api import api
from .models import Statistics
from datetime import datetime




# Create your views here.
@login_required(redirect_field_name=None)
def index(request):
    statistics = Statistics.objects.values().order_by('-date')
    data = {
        'documents': [],
        'indexes': [],
        'size': [],
        'labels': []
    }
    for item in statistics:
        data['documents'].append(item['documents'])
        data['indexes'].append(item['indexes'])
        data['size'].append(item['size'])
        data['labels'].append(item['date'].strftime('%d.%m.%Y'))

    statistic_latest = Statistics.objects.latest('date')

    context = {
        'title': 'Статистика',
        'subtitle': 'Краткая инофрмация касательно проекта',
        'statistic_latest': statistic_latest,
        'statistics': data
    }

    return render(request, 'statistic/index.html', context=context)