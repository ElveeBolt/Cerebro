from django.urls import path
from .views import HelpListView

urlpatterns = [
    path('', HelpListView.as_view(), name='help'),
]
