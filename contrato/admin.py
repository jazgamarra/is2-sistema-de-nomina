from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    # Actualiza 'list_display' para usar 'id' en lugar de 'id_contrato'
    list_display = ['id_contrato', 'id_empleado', 'tipo_contrato', 'salario', 'fecha_inicio', 'fecha_fin', 'contrato_activo']
    search_fields = ('id', 'id_empleado__nombres', 'id_empleado__apellidos')
