from django.urls import path

from .views import StudentEnglishMembershipSelectView, StudentFutureMembershipSelectView, EngPaymentView, FutPaymentView, updateEngTransaction, updateFutTransaction, profile_view
app_name = 'studentmemberships'

urlpatterns = [
    path('profile', profile_view, name="profile"),
	path('english/', StudentEnglishMembershipSelectView.as_view(), name='selectengstudentmem'),
    path('engpay', EngPaymentView, name='engpay'),
    path('future/', StudentFutureMembershipSelectView.as_view(), name='selectfutstudentmem'),
    path('futurepay/', FutPaymentView, name='futurepay'),
    path('eng/<subscription_id>/', updateEngTransaction, name='updatetransactioneng'),
    path('future/<subscription_id>/', updateFutTransaction, name='updatetransactionfut'),
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
