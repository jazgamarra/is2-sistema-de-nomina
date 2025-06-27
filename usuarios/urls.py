from django.urls import path
from .views import login_view, logout_view
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', views.listar_usuarios, name='listar_usuarios'),
    path('nuevo/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
