from django.urls import path

from .views import englishgrades 
app_name = 'grades'

urlpatterns = [
    path('englishgrades/', englishgrades, name="englishgrades"),
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
