from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from homepages.forms import LoginForm, StudentRegistrationForm 
from homepages.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.core.cache import cache


def index(request):
    return render(request, 'homepage/index.html')

def joinus(request):
    return render(request, 'homepage/joinus.html')

def aboutus(request):
    return render(request, 'homepage/aboutus.html')

def studentsignup(request):
    if request.method == 'POST':
        create_user_form = StudentRegistrationForm(request.POST)

        if create_user_form.is_valid():
            new_user = create_user_form.save(commit=False)

            new_user.set_password(
                create_user_form.cleaned_data['password'])
            
            new_user.save()
            
            profile = UserProfile.objects.create(user=new_user, usertype='Child')
            profile.referredby = create_user_form.cleaned_data['referred_by']
            profile.save()

            return render(request, 'homepage/register_done.html', {'new_user': new_user})
        
    else:
        create_user_form = StudentRegistrationForm()

    return render(request, 'homepage/signup.html', {'create_user_form': create_user_form})

def signin(request):
    if request.method =='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next')
                    
                    if next_url:
                        return redirect(next_url) 
        
                    else:
                        return redirect(reverse('studentmemberships:profile'))

                else:
                    return redirect(reverse('homepages:signin'))
#                    return HttpResponse("You're like the limit in this function. DNE!")
            else:
                return redirect(reverse('homepages:signin'))
#                return HttpResponse("If at first you don't succeed, try, try, try again. (Your login is invalid.)")

    else:
        form = LoginForm()
    return render(request, 'homepage/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect(reverse('homepages:index'))

def mission(request):
    return render(request, 'homepage/mission.html')

def how(request):
    return render(request, 'homepage/how.html')

def ourstory(request):
    return render(request, 'homepage/ourstory.html')


def credits(request):
    return render(request, 'homepage/credits.html')

def terms(request):
    return render(request, 'homepage/terms.html')

def parentsignup(request):
    if request.method == 'POST':
        create_user_form = ParentRegistrationForm(request.POST)

        if create_user_form.is_valid():
            new_user = create_user_form.save(commit=False)

            new_user.set_password(
                create_user_form.cleaned_data['password'])
            
            new_user.save()
            profile = UserProfile.objects.create(user=new_user, usertype='Parent')

            return render(request, 'homepage/register_done.html', {'new_user': new_user})
        
    else:
        create_user_form = ParentRegistrationForm()

    return render(request, 'homepage/parentsignup.html', {'create_user_form': create_user_form})
 