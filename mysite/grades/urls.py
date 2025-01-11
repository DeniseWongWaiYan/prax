from django.urls import path

from .views import grades, peer
app_name = 'grades'

urlpatterns = [
    path('grades/', grades, name="grades"),
    path('peer/<username>', peer, name="peer"),
    
    

#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
