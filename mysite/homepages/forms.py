from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.forms import UserCreationForm

from django.utils.translation import gettext as _

class LoginForm(forms.Form):

    username = forms.CharField(max_length=20, label='', initial=_('Username'))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(render_value=True), label='', initial=_('Password'))

class StudentRegistrationForm(forms.ModelForm):
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
    

