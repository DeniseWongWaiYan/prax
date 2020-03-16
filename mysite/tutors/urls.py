from django.urls import path

from .views import tutor_profile, dynamic_stream, indexscreen, tutor_login
app_name = 'tutors'

urlpatterns = [
    path('profile/<slug>', tutor_profile, name="profile"),
    path('login', tutor_login, name="login"),
    path('video/<stream_path>', dynamic_stream , name="videostream"),
    path('stream/<videoslug>', indexscreen)
	
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
