from django import forms
from django.forms.widgets import RadioSelect, Textarea
from django.forms import ModelForm
from .models import Discussion


class DiscussionForm(ModelForm):
     class Meta:
            model = Discussion
            fields = ['discuss']
            
            widgets = {
                    'discuss': forms.Textarea(attrs={'placeholder': 'Add your comment here'})
            }

            