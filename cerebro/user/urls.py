from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='user'),
    path('change-password', views.change_password, name='change_password'),
    path('search-history', views.search_history, name='search_history'),
    path('login-history', views.login_history, name='login_history'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),

    path('admin/statistics', views.AdminStatisticsView.as_view(), name='admin_statistics'),
    path('admin/configurator', views.admin_configurator, name='admin_configurator'),
    path('admin-user-registration', views.admin_user_registration, name='admin_user_registration'),
    path('admin/index', views.AdminIndexView.as_view(), name='admin_index'),
    path('admin/index/<str:index>', views.AdminIndexDetailView.as_view(), name='admin_index_view'),
    path('admin/cluster_tasks', views.AdminClusterTasksView.as_view(), name='admin_cluster_tasks'),

]


