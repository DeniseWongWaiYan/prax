from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.forms import UserCreationForm

from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='', widget=forms.TextInput(attrs={'placeholder': _('Username')}) )
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(render_value=True, attrs={'placeholder': _('Password')}), label='')

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'placeholder': '*******'}))
    confirmpassword = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput(attrs={'placeholder': '*******'}))
    referred_by = forms.CharField(label=_('Referred By'))

    class Meta:
        model = User
        fields = (('username'), ('first_name'), ('last_name'), ('email'))
        help_texts = {
            'email': ("if you would prefer to use your phone instead, just put in your phone number, followed by @p.com"),

        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Anakin帅哥66'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Anakin'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Skywalker'}),
            'email': forms.TextInput(attrs={'placeholder': 'anakin@jedipadawan.com or 86 1065529988@p.com'}),
        }



    def clean_confirmpassword(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirmpassword']:
            raise forms.ValidationError('The passwords you have entered are like Trump and dignity... they don\'t match')
        return cd['confirmpassword']

class ParentRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = (_('username'), _('first_name'), _('last_name'), _('email'))

    def clean_confirmpassword(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirmpassword']:
            raise forms.ValidationError('The passwords you have entered are like Trump and dignity... they don\'t match')
        return cd['confirmpassword']
    

