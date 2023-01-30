from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from api import api
from user.models import History
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from user.models import Login
from databases.models import Database



@receiver(user_logged_in)
def my_callback(request, user, **kwargs):
    login = Login(
        user=user,
        ip=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
        cookies=request.META.get('HTTP_COOKIE')
    )

    login.save()


# Create your views here.
@login_required(redirect_field_name=None)
def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'search/index.html', context=context)


@login_required(redirect_field_name=None)
def results(request):
    query = request.GET.get('q')
    start = request.GET.get('start', 1)
    documents = api.get_documents(query=query)

    if documents is not None:
        paginator = Paginator(documents['data'], settings.RESULTS_PER_PAGE)
        total = documents.get('total')

        try:
            page_obj = paginator.page(start)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    else:
        page_obj = None
        total = 0

    search = History(
        user=request.user,
        query=query,
        total=total
    )
    search.save()

    context = {
        'title': 'Результаты поиска',
        'page_obj': page_obj,
        'query': query,
        'documents': documents
    }

    return render(request, 'search/results.html', context=context)


@login_required(redirect_field_name=None)
def result(request, index, id):
    documents = api.get_document_by_id(index=index, id_=id)
    try:
        database = Database.objects.filter(index=index).get()
    except Database.DoesNotExist:
        database = None

    context = {
        'title': 'Результат',
        'subtitle': 'Детальная информация касательно обьекта',
        'documents': documents,
        'database': database
    }
    return render(request, 'search/result.html', context=context)


@login_required(redirect_field_name=None)
def about(request):
    context = {
        'title': 'О проекте'
    }
    return render(request, 'search/about.html', context=context)


@login_required(redirect_field_name=None)
def error_500(request):
    return render(request, '500.html')
