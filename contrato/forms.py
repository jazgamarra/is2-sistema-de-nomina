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
        self.fields['salario_acordado'].required = False  # ✅ Confirmado opcional

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_fin', "La fecha de fin no puede ser anterior a la fecha de inicio.")
