from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from . models import EnglishCourse

class EnglishCourseListView(ListView):
    model = EnglishCourse

class EnglishCourseDetailView(DetailView):
    model = EnglishCourse
    