from django.shortcuts import render

from .models import EnglishGrades

# Create your views here.
def englishgrades(request):
    
    grades = EnglishGrades.objects.filter(student = request.user).all()
     
    context = {
     'grades': grades,
    }
    
    return render(request, "grades/gradeslist.html", context)