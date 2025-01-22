from django import forms
from .models import ClientQuestion

class ClientQuestionForm(forms.ModelForm):
    class Meta:
        model = ClientQuestion
        fields = ['dialogue_example', 'topic', 'requires_crm', 'tags']  # удалили 'complexity'
        widgets = {
            'dialogue_example': forms.HiddenInput(),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: возраст, python, начинающие'
            }),
            'topic': forms.Select(attrs={'class': 'form-select'}),
        }