from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='user'),
    path('change-password', views.change_password, name='change_password'),
    path('search-history', views.search_history, name='search_history'),
    path('login-history', views.login_history, name='login_history'),
    path('login', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('admin-statistics', views.admin_statistics, name='admin_statistics'),
    path('admin-configurator', views.admin_configurator, name='admin_configurator'),
    path('admin-user-registration', views.admin_user_registration, name='admin_user_registration')
]