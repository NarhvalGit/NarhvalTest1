"""Forms for the prompt agent application."""
from django import forms
from .models import AgentSession


class PromptForm(forms.Form):
    """Form for submitting prompts."""

    prompt = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Typ hier je prompt...',
            'id': 'prompt-input'
        }),
        label='Prompt',
        help_text='Voer je vraag of opdracht in'
    )

    session = forms.ModelChoiceField(
        queryset=AgentSession.objects.filter(is_active=True),
        required=False,
        empty_label='Standaard sessie',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Agent Sessie',
        help_text='Kies een specifieke agent sessie (optioneel)'
    )


class AgentSessionForm(forms.ModelForm):
    """Form for creating/editing agent sessions."""

    class Meta:
        model = AgentSession
        fields = ['name', 'model', 'system_prompt', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'system_prompt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Optionele system prompt voor agent configuratie...'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Naam',
            'model': 'Model',
            'system_prompt': 'System Prompt',
            'is_active': 'Actief',
        }
