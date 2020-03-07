from django.urls import path

from .views import StudentEnglishMembershipSelectView, StudentFutureMembershipSelectView, EngPaymentView
app_name = 'studentmemberships'

urlpatterns = [
	path('eng', StudentEnglishMembershipSelectView.as_view(), name='selectengstudentmem'),
    path('eng/pay', EngPaymentView, name='engpay'),
    path('future', StudentFutureMembershipSelectView.as_view(), name='selectfutstudentmem'),
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
