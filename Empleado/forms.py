# empleados/forms.py
from django import forms
from nomina.models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ["id_departamento","id_contrato",'nombres', 'apellidos', 'cedula', 'fecha_nacimiento', 'telefono', 'email', 'fecha_ingreso', 'activo']
