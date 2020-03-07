from django.urls import path

from .views import StudentEnglishMembershipSelectView, StudentFutureMembershipSelectView
app_name = 'studentmemberships'

urlpatterns = [
	path('eng', StudentEnglishMembershipSelectView.as_view(), name='selectengstudentmem'),
    path('future', StudentFutureMembershipSelectView.as_view(), name='selectfutstudentmem'),
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
