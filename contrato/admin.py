from django.contrib import admin
from .models import Contrato

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['id_contrato', 'id_empleado', 'tipo_contrato', 'salario', 'fecha_inicio', 'fecha_fin', 'contrato_activo']
    list_filter = ['contrato_activo', 'tipo_contrato']  # ✅ Añadido para mejorar la filtración en el admin
    search_fields = ['id_contrato', 'id_empleado__nombres', 'id_empleado__apellidos']  # ✅ Corregido 'id' → 'id_contrato'
