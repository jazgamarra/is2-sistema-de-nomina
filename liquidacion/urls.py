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
    path('empleado/<int:empleado_id>/cargar-conceptos/', views.cargar_conceptos_empleado, name='cargar_conceptos_empleado'),
    path('empleado/<int:empleado_id>/guardar-conceptos/', views.guardar_conceptos, name='guardar_conceptos'),
    path('gestionar-nominas/', views.gestionar_nominas, name='gestionar_nominas'),
    path('generar-nomina/', views.generar_nomina, name='generar_nomina'),
    path('empleados/cargar-conceptos/', views.listar_empleados_para_concepto, name='lista_empleados_concepto'),
]
