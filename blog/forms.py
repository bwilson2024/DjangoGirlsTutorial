from django import forms
from .models import Meditation, Journaling

class MeditationForm(forms.ModelForm):
    class Meta:
        model = Meditation
        fields = ['length', 'impact']

class JournalingForm(forms.ModelForm):
    class Meta:
        model = Journaling
#        fields = ['entry_number', 'date']
        fields = ['entry_number', 'date', 'entry_text']  # Add 'entry_text' to the form fields

        