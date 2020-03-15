from django.urls import path

from .views import tutor_profile
app_name = 'tutors'

urlpatterns = [
    path('profile/<slug>', tutor_profile, name="profile"),
	
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
