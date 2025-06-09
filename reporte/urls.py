from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_reportes, name='menu_reportes'),
    path('sueldos/', views.reporte_sueldos, name='reporte_sueldos'),
    path('conceptos/', views.reporte_conceptos, name='reporte_conceptos'),
    path('costos-empleados/', views.reporte_costos_empleados, name='reporte_costos_empleados'),
    path('', views.menu_reportes, name='menu_reportes'),
    path('costos-mensuales/', views.dashboard_costos_mensuales, name='dashboard_costos_mensuales'),
]
