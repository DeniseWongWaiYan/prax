from django import forms
from django.contrib.auth.models import User
#from .models import StudentProfile
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):

    username = forms.CharField(max_length=20, label='', initial='Username')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(render_value=True), label='', initial='Password')

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_confirmpassword(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirmpassword']:
            raise forms.ValidationError('The passwords you have entered are like Trump and dignity... they don\'t match')
        return cd['confirmpassword']


    

