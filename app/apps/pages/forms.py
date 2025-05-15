from django import forms
from .models import Messages

class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = (
            "name",
            "email",
            "message",
            "interest_service",
        )


class BulkEmailForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'size': '40'}),
        help_text='Asunto del correo electrónico'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        help_text='Contenido del correo electrónico (puede incluir HTML)'
    )
