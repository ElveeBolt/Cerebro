from django.shortcuts import render
from .models import Help, HelpCategory
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(redirect_field_name=None)
def index(request):
    data = []
    categories = HelpCategory.objects.all()
    for category in categories:
        questions = Help.objects.filter(category=category.id).values()
        data.append({
            'id': category.id,
            'category': category.title,
            'questions': questions
        })

    context = {
        'title': 'Помощь',
        'subtitle': 'Страница ответов на часто задаваемые вопросы',
        'data': data
    }
    return render(request, 'help/index.html', context=context)