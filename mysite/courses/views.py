from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, View
from . models import EnglishCourse, FutureCourse 
from studentmemberships.models import EnglishStudentMembershipType, StudentMembership

class EnglishCourseListView(ListView):
    model = EnglishCourse

class EnglishCourseDetailView(DetailView):
    model = EnglishCourse

class FutureCourseListView(ListView):
    model = FutureCourse

class FutureCourseDetailView(DetailView):
    model = FutureCourse
    
#lesson view
class EnglishLessonDetailView(View):
    
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        
        course_qs = EnglishCourse.objects.filter(slug=course_slug)
        if course_qs.exists():
            englishcourse = course_qs.first()
            
        lesson_qs = englishcourse.englishlesson.filter(slug=lesson_slug)
        if lesson_qs.exists():
            englishlesson = lesson_qs.first()
            
        user_membership = StudentMembership.objects.filter(user=request.user).first()
        user_membership_type = user_membership.englishmembership.english_membership_type
        
        course_allowed_mem_types = englishcourse.allowed_memberships.all()
            
        context = {
            'object': None,            
        }
        
        if course_allowed_mem_types.filter(english_membership_type=user_membership_type).exists():
            context = { 'object': englishlesson, }
        
        return render(request, "courses/englishlesson_detail.html", context)
    
    

class FutureLessonDetailView(View):
    
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        
        course_qs = FutureCourse.objects.filter(slug=course_slug)
        if course_qs.exists():
            futurecourse = course_qs.first()
            
        lesson_qs = futurecourse.futurelessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            futurelesson = lesson_qs.first()
            
        user_membership = StudentMembership.objects.filter(user=request.user).first()
        user_membership_type = user_membership.futuremembership.future_membership_type
        
        course_allowed_mem_types = futurecourse.allowed_memberships.all()
            
        context = {
            'object': None,            
        }
        
        if course_allowed_mem_types.filter(future_membership_type=user_membership_type).exists():
            context = {
                'object': futurelesson
            }

        return render(request, "courses/futurelesson_detail.html", context)