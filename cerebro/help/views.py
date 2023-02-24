from django.shortcuts import render
from .models import HelpCategory
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(redirect_field_name=None)
def index(request):
    context = {
        'title': 'Помощь',
        'subtitle': 'Страница ответов на часто задаваемые вопросы',
        'categories': HelpCategory.objects.all()
    }

    return render(request, 'help/index.html', context=context)