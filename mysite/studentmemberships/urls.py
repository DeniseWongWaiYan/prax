from django.urls import path

from .views import StudentEnglishMembershipSelectView, StudentFutureMembershipSelectView, EngPaymentView, EngAlipayView, FutPaymentView, updateEngTransaction, updateFutTransaction, profile_view

from tutors.views import indexscreen

app_name = 'studentmemberships'

urlpatterns = [
    path('profile', profile_view, name="profile"),
	path('english/', StudentEnglishMembershipSelectView.as_view(), name='selectengstudentmem'),
    path('engpay', EngPaymentView, name='engpay'),
    path('engalipay', EngAlipayView, name='engalipay'),
    path('future/', StudentFutureMembershipSelectView.as_view(), name='selectfutstudentmem'),
    path('futurepay/', FutPaymentView, name='futurepay'),
    path('eng/<subscription_id>/', updateEngTransaction, name='updatetransactioneng'),
    path('future/<subscription_id>/', updateFutTransaction, name='updatetransactionfut'),
    path('stream/<videoslug>', indexscreen)
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
