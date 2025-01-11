from django.urls import path

from .views import StudentFutureMembershipSelectView, FutPaymentView, updateFutTransaction, profile_view

from tutors.views import indexscreen

app_name = 'studentmemberships'

urlpatterns = [
    path('profile', profile_view, name="profile"),
	path('future/', StudentFutureMembershipSelectView.as_view(), name='selectfutstudentmem'),
    path('futurepay/', FutPaymentView, name='futurepay'),
    path('future/<subscription_id>/', updateFutTransaction, name='updatetransactionfut'),
#    path('/')
    
#    path('', StudentMembershipFutureSelectView.as_view(), name='selectfuturestudentmem')
]
