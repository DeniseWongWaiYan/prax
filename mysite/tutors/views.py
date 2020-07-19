from django.shortcuts import render

from studentmemberships.models import StudentMembership
from .models import EnglishTutors, FutureTutors

from grades.models import EnglishGrades

from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip

import time


from tutors.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
# Create your views here.

def tutor_profile(request, slug):
	tutor = Tutors.objects.get(slug=slug)

	context = {
		'tutor': tutor,
		'students': StudentMembership.objects.filter(englishtutor=tutor).all()

	}

	return render(request, "tutors/profile.html", context)

def tutor_login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    tutor = Tutors.objects.get(user=user)
                    slug = tutor.slug

                    return redirect(reverse('tutors:profile', kwargs={'slug': slug }))

                else:
                    return HttpResponse("You're like the limit in this function. DNE!")
            else:
                return HttpResponse("If at first you don't succeed, try, try, try again. (Your login is invalid.)")

    else:
        form = LoginForm()
    return render(request, 'homepage/signin.html', {'form': form})

def indexscreen(request, videoslug):
    student = StudentMembership.objects.get(user=request.user)
    tutor = student.englishtutor
    try:
        videoslug = tutor.videoslug
    except:
        videoslug = Tutors.objects.get(user=request.user).videoslug
    
    context = {
	 	'videoslug': videoslug,
	 }
    
    return render(request, "tutors/index.html", context)
     