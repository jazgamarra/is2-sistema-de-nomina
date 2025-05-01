from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_conceptos, name='listar_conceptos'),
    path('crear/', views.crear_concepto, name='crear_concepto'),
    path('editar/<int:pk>/', views.editar_concepto, name='editar_concepto'),
    path('eliminar/<int:pk>/', views.eliminar_concepto, name='eliminar_concepto'),
]
