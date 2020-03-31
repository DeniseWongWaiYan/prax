from django import forms

from .models import VocabularyWord

class AddVocab(forms.ModelForm):
    
    class Meta:
        model = VocabularyWord
        fields = ('new_word', 'definition','comments')
 