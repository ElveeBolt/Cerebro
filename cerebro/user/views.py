from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import History, Login
from statistic.models import Statistics
from api import api
from django.conf import settings
from .services.Configurator import Configurator
from .forms import SignUpForm



# Create your views here.
@login_required(redirect_field_name=None)
def index(request):
    history_search_count = History.objects.filter(user=request.user).count()
    history_login_count = Login.objects.filter(user=request.user).count()
    context = {
        'title': ' Мой профиль',
        'subtitle': 'Детальная информация о пользователе',
        'history_search_count': history_search_count,
        'history_login_count': history_login_count
    }

    return render(request, 'user/index.html', context=context)


@login_required(redirect_field_name=None)
def change_password(request):
    context = {
        'title': 'Смена пароля',
        'subtitle': 'Страница смены пароля',
        'form': []
    }
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_repeat = request.POST.get("new_password_repeat")
        if check_password(old_password, user.password):
            if new_password != new_password_repeat:
                context['form'].append('Введенные вами новые пароли не совпадают')
            else:
                try:
                    validate_password(new_password, password_validators=None)
                    user.set_password(new_password)
                    user.save()
                except ValidationError as e:
                    context['form'] = e
        else:
            context['form'].append('Введенный вами текущий пароль неверный. Повторите попытку ещё раз')

    return render(request, 'user/change_password.html', context=context)


@login_required(redirect_field_name=None)
def search_history(request):
    history = History.objects.filter(user=request.user).values().order_by('-date')

    context = {
        'title': 'История поиска',
        'subtitle': 'Информация касательно ваших поисковых запросов',
        'history': history
    }

    return render(request, 'user/search_history.html', context=context)


@login_required(redirect_field_name=None)
def login_history(request):
    history = Login.objects.filter(user=request.user).values().order_by('-date')

    context = {
        'title': 'История посещений',
        'subtitle': 'Информация касательно активности профиля',
        'history': history
    }

    return render(request, 'user/login_history.html', context=context)



@login_required(redirect_field_name=None)
def admin_statistics(request):

    status_update = None
    if request.GET.get('update'):
        status_update = 'Данные успешно обновлены'
        statistics = Statistics(
            documents=api.get_total_documents(),
            indexes=api.get_total_indices(),
            size=api.get_indexes_size()
        )
        statistics.save()

    history = Statistics.objects.values().order_by('-date')

    context = {
        'title': 'История посещений',
        'subtitle': 'Информация касательно активности профиля',
        'history': history,
        'status_update': status_update
    }

    return render(request, 'user/admin_statistics.html', context=context)


@login_required(redirect_field_name=None)
def admin_user_registration(request):
    context = {
        'title': 'Регистрация пользователя',
        'subtitle': 'Создание нового пользователя',
        'form_success': False
    }

    form = SignUpForm(request.POST)

    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.name = form.cleaned_data.get('name')
        user.profile.division = form.cleaned_data.get('division')
        user.profile.comment = form.cleaned_data.get('comment')
        user.save()
        context['form_success'] = True
        form = SignUpForm()
    else:
        form = SignUpForm()

    context['form'] = form

    return render(request, 'user/admin_user_registration.html', context=context)


@login_required(redirect_field_name=None)
def admin_configurator(request):
    context = {
        'title': 'Конфигуратор источников',
        'subtitle': 'Создание конфигурационных файлов для источника данных',
        'mappings': settings.MAPPINGS
    }

    if request.method == 'POST':
        config = request.POST.get("database")
        mappings = request.POST.getlist('mappings')
        configurator = Configurator(mappings=mappings, config=config)
        download = configurator.generate_zip()

        context['download'] = download

    return render(request, 'user/admin_configurator.html', context=context)
