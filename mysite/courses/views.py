from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, View
from courses.models import FutureCourse, Forum, Discussion, FutureLesson
from studentmemberships.models import FutureStudentMembershipType, StudentMembership
from grades.models import FutureGrades
from vocab.models import VocabularyWord
from homepages.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DiscussionForm

class FutureCourseListView(LoginRequiredMixin, ListView):
    model = FutureCourse
#    redirect_field_name = 'en/courses/future'


class FutureCourseDetailView(LoginRequiredMixin, DetailView):
    model = FutureCourse

class FutureLessonDetailView(LoginRequiredMixin, View):
    
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        
        course_qs = FutureCourse.objects.filter(slug=course_slug)
        if course_qs.exists():
            futurecourse = course_qs.first()
            
        lesson_qs = futurecourse.futurelessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            futurelesson = lesson_qs.first()
            
        user_membership = StudentMembership.objects.filter(user=request.user).first()
#        if user_membership.futuremembership is not None:
        user_membership_type = user_membership.futuremembership.future_membership_type
#        else:
#            user_membership_type = 'Future No'
        
        
        course_allowed_mem_types = futurecourse.allowed_memberships.all()
        
        
        context = {
            'object': None, 
        }
        
        
        if course_allowed_mem_types.filter(future_membership_type=user_membership_type).exists():
            words = VocabularyWord.objects.filter(student__isnull=True, lesson = futurelesson)
            
            secrets = VocabularyWord.objects.filter(student=request.user, lesson = futurelesson)
            
            students_in_group = StudentMembership.objects.filter(group=request.user.studentmembership.group).exclude(user=request.user)
            
            forum = Forum.objects.filter(group=request.user.studentmembership.group, lesson=futurelesson) 
            

            context = {
                'object': futurelesson,
                'words': words,
                'students_in_group': students_in_group,
                'secrets': secrets,  
                'forum': forum
            } 

        return render(request, "courses/futurelesson_detail.html", context)
    

def ForumList(request):
    
    forumlist = Forum.objects.filter(group=request.user.studentmembership.group).order_by('-date_created')
    
        
    context = {
        'forumlist': forumlist,
        
    }
    
    return render(request, "courses/forumlist.html", context)
    
def ForumView(request, lesson_slug, group_slug, topic_slug):
    lesson = FutureLesson.objects.get(slug=lesson_slug)
    
    forum = Forum.objects.get(topicslug=topic_slug, group=request.user.studentmembership.group, lesson=lesson) 
    
    discussion = Discussion.objects.filter(forum=forum).order_by('date_created')
    
    if request.method == "POST":
        form = DiscussionForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.student = request.user
            post.forum = forum
            post.save()

            return redirect(request.path)


        else:
            form = DiscussionForm()
    
    
    context = {
        'lesson': lesson,
        'forum': forum,
        'discussion': discussion,
        'form': DiscussionForm,
    }
    
    return render(request, "courses/forum.html", context)


        

    