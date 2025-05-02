from django.contrib import admin
from .models import Concepto

# Register your models here.
@admin.register(Concepto)
class ConceptoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'es_fijo', 'es_deb_cred', 'porcentaje', 'permite_cuotas', 'cant_cuotas']
    list_filter = ['es_fijo', 'es_deb_cred', 'permite_cuotas']  # Filtros útiles para la interfaz
    search_fields = ['descripcion']  # Permite buscar por la descripción
