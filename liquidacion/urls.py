from django.urls import path,include
from . import views

concepto_patterns = [
    path('', views.listar_conceptos, name='listar_conceptos'),
    path('crear/', views.crear_concepto, name='crear_concepto'),
    path('editar/<int:pk>/', views.editar_concepto, name='editar_concepto'),
    path('eliminar/<int:pk>/', views.eliminar_concepto, name='eliminar_concepto'),
]

urlpatterns = [
    path('reportes/empleados/', views.listar_empleados_reporte, name='listar_empleados_reporte'),
    path('reportes/empleado/<int:empleado_id>/', views.ver_nomina_empleado, name='ver_nomina_empleado'),
    path('concepto/', include((concepto_patterns, 'concepto'))),
]