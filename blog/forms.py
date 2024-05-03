from django import forms
from .models import Meditation, Journaling, Post

class MeditationForm(forms.ModelForm):
    class Meta:
        model = Meditation
        fields = ['length', 'impact']

class JournalingForm(forms.ModelForm):
    class Meta:
        model = Journaling
#        fields = ['entry_number', 'date']
        fields = ['entry_number', 'date', 'entry_text']  # Add 'entry_text' to the form fields

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)        

        