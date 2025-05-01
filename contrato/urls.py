from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_contratos, name='listar_contratos'),  # Ruta para listar contratos
    path('crear/', views.crear_contrato, name='crear_contrato'),  # Ruta para crear un contrato
    path('editar/<int:pk>/', views.editar_contrato, name='editar_contrato'),  # Ruta para editar contrato por su ID
    path('eliminar/<int:pk>/', views.eliminar_contrato, name='eliminar_contrato'),  # Ruta para eliminar contrato por su ID
]
