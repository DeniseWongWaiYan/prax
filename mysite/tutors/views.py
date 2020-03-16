from django.shortcuts import render

from studentmemberships.models import StudentMembership
from .models import Tutors

from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import cv2
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

def get_frame():
    camera =cv2.VideoCapture(0) 
    while True:
        _, img = camera.read()
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    del(camera)
    
def indexscreen(request, videoslug): 
	 student = StudentMembership.objects.get(user=request.user)
	 tutor = student.englishtutor
	 videoslug = tutor.videoslug

	 context = {
	 	'videoslug': videoslug,
	 }

	 return render(request, "tutors/screens.html", context)
    # try:
    # 	template = "screens.html"
    # 	return render(request, template)
    # except:
    #     pass

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"
