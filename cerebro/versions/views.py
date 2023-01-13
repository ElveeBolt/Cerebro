from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Version


# Create your views here.
@login_required(redirect_field_name=None)
def index(request):
    versions = Version.objects.all().order_by('-date')
    context = {
        'title': 'История версий',
        'subtitle': 'Информация касательно выпусков и обновлений Cerebro',
                    'versions': versions
    }
    return render(request, 'versions/index.html', context=context)
