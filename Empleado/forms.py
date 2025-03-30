from django import forms
from nomina.models import Empleado, Departamento, Contrato

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['id_departamento', 'id_cargo', 'nombres', 'apellidos', 'cedula', 'fecha_nacimiento', 'telefono', 'email', 'fecha_ingreso', 'activo']

        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los nombres'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los apellidos'
            }),
            'cedula': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cédula'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la fecha de nacimiento',
                'type': 'date'  # para que se vea bien
            }),
            'telefono': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el email'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la fecha de ingreso',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'id_departamento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'id_cargo': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
