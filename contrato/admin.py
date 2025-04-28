from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    # Actualiza 'list_display' para usar 'id' en lugar de 'id_contrato'
    list_display = ('id', 'id_empleado', 'tipo_contrato', 'fecha_inicio', 'fecha_fin', 'salario_acordado', 'contrato_activo')
    search_fields = ('id', 'id_empleado__nombres', 'id_empleado__apellidos')
