from django import forms
from empleado.models import Empleado
import re
from datetime import date
from .models import Departamento


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'id_departamento',
            #'id_cargo', 
            'nombres',
            'apellidos',
            'cedula',
            'fecha_nacimiento',
            'telefono',
            'email',
            'fecha_ingreso',
            'activo',
            'hijos_menores_18',  
            'aplica_ips',        
        ]

        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese los nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese los apellidos'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cédula'}),
            'fecha_nacimiento': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Seleccione la fecha de nacimiento', 'type': 'date'},
                format='%Y-%m-%d'),            
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el email'}),
            'fecha_ingreso': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Seleccione la fecha de ingreso', 'type': 'date'},
                format='%Y-%m-%d'),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'id_departamento': forms.Select(attrs={'class': 'form-control'}),
            'id_cargo': forms.Select(attrs={'class': 'form-control'}),
            'hijos_menores_18': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad de hijos menores de 18'}),
            'aplica_ips': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d']
        self.fields['fecha_ingreso'].input_formats = ['%Y-%m-%d']

    # 🚨 Validar nombres y apellidos (evitar inyección SQL y caracteres extraños)
    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombres):
            raise forms.ValidationError("Los nombres solo pueden contener letras y espacios.")
        return nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellidos):
            raise forms.ValidationError("Los apellidos solo pueden contener letras y espacios.")
        return apellidos

    # 🚨 Validar que la cédula solo contenga números
    def clean_cedula(self):
        cedula = str(self.cleaned_data.get('cedula'))
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo puede contener números.")
        return cedula

    # 🚨 Validar que la fecha de nacimiento no sea futura
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento and fecha_nacimiento > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fecha_nacimiento

    # 🚨 Validar que el email tenga un formato correcto
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError("Ingrese un correo válido.")
        return email


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['id_departamento', 'departamento']
        widgets = {
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'id_departamento': forms.NumberInput(attrs={'class': 'form-control'}),
        }
