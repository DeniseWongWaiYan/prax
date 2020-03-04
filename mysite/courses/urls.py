from django.urls import path

from .views import EnglishCourseListView, EnglishCourseDetailView

urlpatterns = [
    path('', EnglishCourseListView.as_view(), name='EnglishListView'),
    path('<slug>', EnglishCourseDetailView.as_view(), name='EnglishListView'),
]
