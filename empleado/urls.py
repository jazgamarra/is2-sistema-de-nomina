
from django.urls import path
from . import views

urlpatterns = [
    # Rutas para empleados
    path('', views.listar_empleados, name='listar_empleados'),
    path('crear/', views.crear_empleado, name='crear_empleado'),
    path('editar/<int:pk>/', views.editar_empleado, name='editar_empleado'),
    path('eliminar/<int:pk>/', views.eliminar_empleado, name='eliminar_empleado'),

    # Rutas para departamentos
    path('departamentos/', views.listar_departamentos, name='listar_departamentos'),
    path('departamentos/crear/', views.crear_departamento, name='crear_departamento'),
    path('departamentos/<int:pk>/editar/', views.editar_departamento, name='editar_departamento'),
    path('departamentos/<int:pk>/eliminar/', views.eliminar_departamento, name='eliminar_departamento'),
]
