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
    path('gestionar-nominas/', views.gestionar_nominas, name='gestionar_nominas'),
    path('generar-nomina/', views.generar_nomina, name='generar_nomina'),
    path('empleado/<int:empleado_id>/editar-conceptos/', views.editar_conceptos_empleado, name='editar_conceptos_empleado'),
    path('empleados/editar-conceptos/', views.listar_empleados_para_concepto, name='listar_empleados_para_concepto'),
    path('empleado/<int:empleado_id>/ver-nomina/', views.ver_nomina_empleado, name='ver_nomina_empleado'),
    # rutas para generar recibos de pago
    path('empleado/<int:empleado_id>/recibos/', views.recibo_pago, name='recibo_pago'),
    path('empleado/<int:empleado_id>/recibos/<int:liquidacion_id>/pdf/', views.descargar_recibo_pdf, name='descargar_recibo_pdf'),
    path('nomina/pdf/', views.generar_pdf_nomina_listado, name='generar_pdf_nomina_listado'),

]
