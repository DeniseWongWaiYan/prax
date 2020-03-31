from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import DocumentForm
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import EnglishGrades

# Create your views here.
def englishgrades(request):
    
    grades = EnglishGrades.objects.filter(student = request.user).all()
     
    context = {
     'grades': grades,
    }
    
    return render(request, "grades/gradeslist.html", context)

def futuregrades(request):
    
    grades = FutureGrades.objects.filter(student = request.user).all()
     
    context = {
     'grades': grades,
    }
    
    return render(request, "grades/gradeslist.html", context)

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
    
        if form.is_valid():
            form.instance.student = request.user
            form.save()
            return redirect(reverse('grades:englishgrades'))
    else:
        form = DocumentForm()
    return render(request, 'grades/model_form_upload.html', {
        'form': form
    })

