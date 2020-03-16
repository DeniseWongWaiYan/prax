from django.urls import path

from .views import ParentMembershipSelectView, ParentPaymentView, updateTransaction, profile_view
app_name = 'parents'

urlpatterns = [
    path('profile', profile_view, name="profile"),
	path('parentselect/', ParentMembershipSelectView.as_view(), name='selectparentmem'),
    path('parentpay', ParentPaymentView, name='parentpay'),
    path('eng/<subscription_id>/', updateTransaction, name='updatetransaction'),
    
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
