from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('results', views.results, name='results'),
    path('result/<str:index>/<str:id>', views.result,  name='result'),
    path('about', views.AboutView.as_view(), name='about'),
]