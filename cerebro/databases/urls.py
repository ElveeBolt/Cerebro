from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='databases'),
    path('<str:index>', views.database, name='database'),
]