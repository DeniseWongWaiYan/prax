from django.urls import path

from .views import FutureCourseListView, FutureCourseDetailView, FutureLessonDetailView, ForumView, ForumList

app_name = 'courses'

urlpatterns = [
    path('future', FutureCourseListView.as_view(), name='futurelist'),
    path('forumlist', ForumList, name='forumlist'),
    path('future/<slug>', FutureCourseDetailView.as_view(), name='futuredetail'),
    path('future/<course_slug>/<lesson_slug>', FutureLessonDetailView.as_view(), name='futurelessondetail'), 
    path('future/<lesson_slug>/<group_slug>/<topic_slug>', ForumView, name='forum'), 

    
]

