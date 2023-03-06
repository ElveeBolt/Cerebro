from django.urls import path
from .views import DatabaseListView, DatabaseView, PostView

urlpatterns = [
    path('', DatabaseListView.as_view(), name='databases'),
    path('<int:pk>', DatabaseView.as_view(), name='database'),
    path('post/<int:pk>', PostView.as_view(), name='post'),
]