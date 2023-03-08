from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from .models import History, Login, User
from statistic.models import Statistics
from api import api
from django.conf import settings
from .services.Configurator import Configurator
from .forms import SignUpForm, SignInForm, ChangePasswordForm, StatisticForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


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
        'form': ChangePasswordForm(request.user)
    }
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            context['form'] = ChangePasswordForm(request.user)
        else:
            context['form'] = form

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


class AdminStatisticsView(LoginRequiredMixin, CreateView):
    model = Statistics
    form_class = StatisticForm
    template_name = 'user/admin/statistics.html'
    success_url = '#'
    extra_context = {
        'title': 'История посещений',
        'subtitle': 'Информация касательно активности профиля'
    }

    def get_initial(self):
        return {
            'documents': api.get_total_documents(),
            'indexes': api.get_total_indices(),
            'size': api.get_indexes_size(),
            'users': User.objects.all().count(),
            'queries': History.objects.all().count()
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statistics'] = Statistics.objects.order_by('-date')
        return context


@login_required(redirect_field_name=None)
def admin_user_registration(request):
    context = {
        'title': 'Регистрация пользователя',
        'subtitle': 'Создание нового пользователя',
        'form': SignUpForm(),
        'form_success': False
    }

    form = SignUpForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            context['form_success'] = True
            context['form'] = SignUpForm()
        else:
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


class AdminIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user/admin/index.html'
    extra_context = {
        'title': 'Состояние источников',
        'subtitle': 'Просмотр данных об источниках в реальном времени',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['indexes'] = api.get_indexes_info()
        return context


class AdminIndexDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'user/admin/index_view.html'
    extra_context = {
        'title': 'Разметка полей источника',
        'subtitle': 'Детали разметки полей источника данных',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapping'] = api.get_index_mapping(self.kwargs['index'])
        return context


class AdminClusterTasksView(LoginRequiredMixin, TemplateView):
    template_name = 'user/admin/cluster_tasks.html'
    extra_context = {
        'title': 'Состояние кластера',
        'subtitle': 'Информация о текущих задачах кластера Elastic',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = api.get_elasticsearch_tasks()
        return context


def login(request):
    context = {
        'title': 'Авторизация',
        'subtitle': 'Для начала использования возможностей Cerebro выполните вход в систему',
        'form': SignInForm()
    }

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Вы пытаетесь войти под несуществующими данными')

        context['form'] = form

    return render(request, 'user/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/user/login')
