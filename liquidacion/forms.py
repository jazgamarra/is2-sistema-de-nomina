from django import forms
from .models import Concepto

class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = [
            'descripcion',
            'es_fijo',
            'es_deb_cred',
            'porcentaje',
            'permite_cuotas',
            'cant_cuotas',
        ]
        widgets = {
            'porcentaje': forms.NumberInput(attrs={'type': 'number', 'step': '0.01'}),
            'cant_cuotas': forms.NumberInput(attrs={'type': 'number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['porcentaje'].required = False  # Hacer opcional si es necesario
        self.fields['cant_cuotas'].required = False  # Hacer opcional si es necesario
