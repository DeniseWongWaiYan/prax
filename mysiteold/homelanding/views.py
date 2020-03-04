from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from homelanding.forms import LoginForm, StudentRegistrationForm, UserEdit, ProfileEdit, ParentRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import StudentProfile, ParentProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import redirect

import stripe

def index(request):
    return render(request, 'homelanding/index.html')

def joinus(request):
    return render(request, 'homelanding/joinus.html')

def aboutus(request):
    return render(request, 'homelanding/aboutus.html')

def studentsignup(request):
    if request.method == 'POST':
        create_user_form = StudentRegistrationForm(request.POST)

        if create_user_form.is_valid():
            new_user = create_user_form.save(commit=False)

            new_user.set_password(
                create_user_form.cleaned_data['password'])
            
            new_user.save()
            profile = StudentProfile.objects.create(user=new_user)

            return render(request, 'homelanding/register_done.html', {'new_user': new_user})
        
    else:
        create_user_form = StudentRegistrationForm()

    return render(request, 'homelanding/signup.html', {'create_user_form': create_user_form})

def parentsignup(request):
    if request.method == 'POST':
        create_user_form = ParentRegistrationForm(request.POST)

        if create_user_form.is_valid():
            new_user = create_user_form.save(commit=False)

            new_user.set_password(
                create_user_form.cleaned_data['password'])

            new_user.save()
            profile = ParentProfile.objects.create(user=new_user)

            return render(request, 'homelanding/register_done.html', {'new_user': new_user})
        
    else:
        create_user_form = ParentRegistrationForm()

    return render(request, 'homelanding/signupparent.html', {'create_user_form': create_user_form})


def signin(request):
    if request.method =='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(student_profile_view)

                else:
                    return HttpResponse("You're like the limit in this function. DNE!")
            else:
                return HttpResponse("If at first you don't succeed, try, try, try again. (Your login is invalid.)")

    else:
        form = LoginForm()
    return render(request, 'homelanding/signin.html', {'form': form})

