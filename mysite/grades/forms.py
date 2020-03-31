from django import forms
from .models import EnglishGrades


class DocumentForm(forms.ModelForm):
    class Meta:
        model = EnglishGrades
        fields = ('lesson', 'upload')
        
    