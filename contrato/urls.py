from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_contratos, name='listar_contratos'),
    path('empleado/<int:empleado_id>/', views.listar_contratos_empleado, name='listar_contratos_empleado'),  # ✅ Agregada vista que ya estaba definida
    path('crear/', views.crear_contrato, name='crear_contrato'),
    path('editar/<int:pk>/', views.editar_contrato, name='editar_contrato'),
    path('eliminar/<int:pk>/', views.eliminar_contrato, name='eliminar_contrato'),
]
