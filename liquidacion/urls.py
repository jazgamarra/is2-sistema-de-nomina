from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas
    path('', views.listar_conceptos, name='listar_conceptos'),  # Para liquidacion/
    path('reportes/empleados/', views.listar_empleados_reporte, name='listar_empleados_reporte'),
    path('reportes/empleado/<int:empleado_id>/', views.ver_nomina_empleado, name='ver_nomina_empleado'),
    # Rutas relacionadas con concepto
    path('concepto/', views.listar_conceptos, name='listar_conceptos'),
    path('concepto/crear/', views.crear_concepto, name='crear_concepto'),
    path('concepto/editar/<int:pk>/', views.editar_concepto, name='editar_concepto'),
    path('concepto/eliminar/<int:pk>/', views.eliminar_concepto, name='eliminar_concepto'),
]
