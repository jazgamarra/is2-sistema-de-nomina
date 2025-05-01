from django import forms
from .models import Contrato

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            'id_empleado',
            'tipo_contrato',
            'salario',
            'salario_acordado',
            'fecha_inicio',
            'fecha_fin',
            'tiene_beneficios',
            'contrato_activo',
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'salario': forms.NumberInput(attrs={'type': 'number', 'step': '0.01'}),
            'salario_acordado': forms.NumberInput(attrs={'type': 'number', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que 'salario_acordado' sea opcional
        self.fields['salario_acordado'].required = False
