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
