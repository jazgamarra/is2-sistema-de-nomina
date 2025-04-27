from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_inicio, name='menu_inicio'),
]
