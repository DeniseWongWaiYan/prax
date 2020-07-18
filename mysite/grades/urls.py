from django.urls import path

from .views import model_form_upload, grades
app_name = 'grades'

urlpatterns = [
    path('grades/', grades, name="grades"),
    path('enghwupload/', model_form_upload, name="enghwupload"),
    path('futurehwupload/', model_form_upload, name="futurehwupload"),
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
