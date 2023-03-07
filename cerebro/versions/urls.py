from django.urls import path
from .views import VersionListView

urlpatterns = [
    path('', VersionListView.as_view(), name='versions'),
]