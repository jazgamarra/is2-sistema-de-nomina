from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu_reportes, name='menu_reportes'),
    path('conceptos/', views.reporte_conceptos, name='reporte_conceptos'),
    path('costos-empleados/', views.reporte_costo_empleado, name='reporte_costo_empleado'),
    path('costos-mensuales/', views.dashboard_general, name='dashboard_costos_mensuales'),
]
