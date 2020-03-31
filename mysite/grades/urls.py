from django.urls import path

from .views import englishgrades, futuregrades, model_form_upload
app_name = 'grades'

urlpatterns = [
    path('englishgrades/', englishgrades, name="englishgrades"),
    path('enghwupload/', model_form_upload, name="enghwupload"),
    path('futuregrades/', englishgrades, name="futuregrades"),
    path('futurehwupload/', model_form_upload, name="futurehwupload"),
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
