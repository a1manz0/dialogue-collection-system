from django import forms
from .models import Dialogue, Message

class DialogueForm(forms.ModelForm):
    class Meta:
        model = Dialogue
        fields = ['topic', 'requires_crm']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'requires_crm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['author', 'text']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите сообщение...'
            }),
        }

class DialogueWithMessagesForm(DialogueForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_forms = []
        
        if self.instance.pk:  # если редактируем существующий диалог
            for message in self.instance.messages.all():
                self.message_forms.append(MessageForm(instance=message))

    def save(self, commit=True):
        dialogue = super().save(commit=commit)
        
        # Сохраняем сообщения
        if commit and self.message_forms:
            for form in self.message_forms:
                if form.is_valid():
                    message = form.save(commit=False)
                    message.dialogue = dialogue
                    message.save()
                    
        return dialogue