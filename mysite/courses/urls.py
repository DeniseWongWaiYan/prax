from django.urls import path

from .views import EnglishCourseListView, EnglishCourseDetailView, FutureCourseListView, FutureCourseDetailView, EnglishLessonDetailView
app_name = 'courses'

urlpatterns = [
    path('english', EnglishCourseListView.as_view(), name='englishlist'),
    path('future', FutureCourseListView.as_view(), name='futurelist'),
    path('english/<slug>', EnglishCourseDetailView.as_view(), name='englishdetail'),
    path('future/<slug>', FutureCourseDetailView.as_view(), name='futuredetail'),
    path('english/<course_slug>/<lesson_slug>', EnglishLessonDetailView.as_view(), name='englishlessondetail'), 
]
