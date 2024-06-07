from django import forms
from .models import Cash_registers

class CashRegisterForm(forms.ModelForm):
    amount_to_deduct = forms.FloatField(label='Näçe aýyrmaly', required=False)

    class Meta:
        model = Cash_registers
        fields = '__all__'