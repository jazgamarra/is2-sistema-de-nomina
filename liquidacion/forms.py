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
                'type': 'number', 'step': '1', 'class': 'form-control',
                'placeholder': 'Ej: 25 (se guarda como 25%)'
            }),
            'cant_cuotas': forms.NumberInput(attrs={'class': 'form-control'}),
            'es_fijo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permite_cuotas': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_permite_cuotas'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['es_deb_cred'] = forms.ChoiceField(
            choices=[(True, 'Crédito'), (False, 'Débito')],
            widget=forms.Select(attrs={'class': 'form-select'}),
            label="Tipo de Concepto"
        )

        self.fields['mostrar_porcentaje'] = forms.BooleanField(
            required=False,
            label="En caso de ser un descuento... ¿El empleado cubre solo un porcentaje?",
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_mostrar_porcentaje'})
        )

        self.fields['porcentaje'].required = False
        self.fields['cant_cuotas'].required = False

        if 'instance' in kwargs and kwargs['instance']:
            self.fields['es_deb_cred'].initial = kwargs['instance'].es_deb_cred

def clean(self):
    cleaned_data = super().clean()
    permite_cuotas = cleaned_data.get("permite_cuotas")
    mostrar_porcentaje = cleaned_data.get("mostrar_porcentaje")

    if not permite_cuotas:
        cleaned_data["cant_cuotas"] = 1

    if not mostrar_porcentaje:
        cleaned_data["porcentaje"] = 0

    return cleaned_data

def clean_porcentaje(self):
    val = self.cleaned_data.get('porcentaje')
    if val is not None:
        return val / 100  # ejemplo: 25 → 0.25
    return val
