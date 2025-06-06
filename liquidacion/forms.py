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
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'porcentaje': forms.NumberInput(attrs={
                'type': 'number', 'step': '0.01', 'class': 'form-control'
            }),
            'cant_cuotas': forms.NumberInput(attrs={'class': 'form-control'}),
            'es_fijo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permite_cuotas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['es_deb_cred'] = forms.ChoiceField(
            choices=[(True, 'Crédito'), (False, 'Débito')],
            widget=forms.Select(attrs={'class': 'form-select'}),
            label="Tipo de Concepto"
        )

        self.fields['porcentaje'].required = False
        self.fields['cant_cuotas'].required = False

        if 'instance' in kwargs and kwargs['instance']:
            self.fields['es_deb_cred'].initial = kwargs['instance'].es_deb_cred
