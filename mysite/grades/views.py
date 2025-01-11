from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Avg
from django.conf import settings
from studentmemberships.views import rank


from .models import FutureGrades, FutCert

# Create your views here.
def grades(request):
    
    futgrades = FutureGrades.objects.filter(student = request.user).all()
    certs = FutCert.objects.filter(student=request.user).all()

    creativity = FutureGrades.objects.filter(student = request.user).aggregate(Avg('creativity'))['creativity__avg']
    
    critical_thinking = FutureGrades.objects.filter(student = request.user).aggregate(Avg('critical_thinking'))['critical_thinking__avg']
    
    communication = FutureGrades.objects.filter(student = request.user).aggregate(Avg('communication'))['communication__avg']
    
    collaboration = FutureGrades.objects.filter(student = request.user).aggregate(Avg('collaboration'))['collaboration__avg']
    
    
    avgcreativity = FutureGrades.objects.all().aggregate(Avg('creativity'))['creativity__avg']

    avgct = FutureGrades.objects.all().aggregate(Avg('critical_thinking'))['critical_thinking__avg']

    
    avcomm = FutureGrades.objects.all().aggregate(Avg('communication'))['communication__avg']

    avcollab = FutureGrades.objects.all().aggregate(Avg('collaboration'))['collaboration__avg']
    
    rank1 = rank(request)
    
    
    context = {
    'futuregrades': futgrades,
    'creativity': creativity,
    'critical_thinking': critical_thinking,
    'communication': communication,
    'collaboration': collaboration,
    'avgcreativity': avgcreativity,
    'avgct':avgct, 
    'avcomm':avcomm,
    'avcollab':avcollab,
    'certs': certs,
    'points': rank1['points'],
    'rank': rank1['rank'],
    'left': rank1['left'],
    }
    
    return render(request, "grades/gradeslist.html", context)



def peer(request, username):
    
    enggrades = EnglishGrades.objects.filter(student = username).all()
    futgrades = FutureGrades.objects.filter(student = username).all()
    certs = FutCert.objects.filter(student=username).all()

    creativity = FutureGrades.objects.filter(student = username).aggregate(Avg('creativity'))['creativity__avg']
    
    critical_thinking = FutureGrades.objects.filter(student = username).aggregate(Avg('critical_thinking'))['critical_thinking__avg']
    
    communication = FutureGrades.objects.filter(student = username).aggregate(Avg('communication'))['communication__avg']
    
    collaboration = FutureGrades.objects.filter(student = username).aggregate(Avg('collaboration'))['collaboration__avg']
    
    
    avgcreativity = FutureGrades.objects.all().aggregate(Avg('creativity'))['creativity__avg']

    avgct = FutureGrades.objects.all().aggregate(Avg('critical_thinking'))['critical_thinking__avg']

    
    avcomm = FutureGrades.objects.all().aggregate(Avg('communication'))['communication__avg']

    avcollab = FutureGrades.objects.all().aggregate(Avg('collaboration'))['collaboration__avg']

    
    context = {
    'futuregrades': futgrades,
    'creativity': creativity,
    'critical_thinking': critical_thinking,
    'communication': communication,
    'collaboration': collaboration,
    'avgcreativity': avgcreativity,
    'avgct':avgct, 
    'avcomm':avcomm,
    'avcollab':avcollab,
    'certs': certs,
    'peer': peer,
    }
    
    return render(request, "grades/peergrades.html", context)

#
#def englishgrades(request):
#    
#    grades = EnglishGrades.objects.filter(student = request.user).all()
#     
#    context = {
#     'grades': grades,
#    }
#    
#    return render(request, "grades/gradeslist.html", context)
#
#def futuregrades(request):
#    
#    grades = FutureGrades.objects.filter(student = request.user).all()
#     
#    context = {
#     'futuregrades': grades,
#    }
#    
#    return render(request, "grades/gradeslist.html", context)

