from django.shortcuts import render

from django.views.generic import ListView, View

from .models import EnglishStudentMembershipType, FutureStudentMembershipType, StudentMembership, StudentEnglishSubscription

def get_user_eng_mem(request):
    eng_mem_qs = StudentMembership.objects.filter(user=request.user)
    if eng_mem_qs.exists():
        return eng_mem_qs.first()
    return None

def get_user_eng_subscription(request):
    user_sub_qs = StudentEnglishSubscription.objcts.filter(englishmembershiptype=get_user_eng_mem(request))
    
    if user_sub_qs.exists():
        user_sub_qs = user_sub_qs.first()
        return user_sub_qs
    return None

def get_user_fut_mem(request):
    fut_mem_qs = StudentMembership.objects.filter(user=request.user)
    if fut_mem_qs.exists():
        return fut_mem_qs.first()
    return None
def get_user_future_subscription(request):
    user_sub_qs = StudentFutureSubscription.objcts.filter(futuremembershiptype=get_user_eng_mem(request))
    
    if user_sub_qs.exists():
        user_sub_qs = user_sub_qs.first()
        return user_sub_qs
    return None

class StudentEnglishMembershipSelectView(ListView):
    model = EnglishStudentMembershipType
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_eng_mem(self.request)
        context['current_membership'] = str(current_membership.englishmembership)
        return context
        
    def post(self, request, **kwargs):
        selected_membership = request.POST.get('english_membership_type')
        eng_membership = get_user_eng_mem(request)
        eng_subscription = get_user_eng_subscription(request)
        
        selected_membership_qs = EnglishStudentMembershipType.objects.filter(english_membership_type=selected_membership_type)
        
#        validation
        
        if eng_membership.englishmembership == selected_membership:
            if eng_subscription != None:
                messages.info(request, 'You already have this membership. Your next payment is die {}'.format('get this valeu from stripe'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        request.session['selected_membership_type'] = selected_membership.english_membership_type
        
        return HttpResponseRedirect(reverse('studentmemberships:paymenteng'))
         
class StudentFutureMembershipSelectView(ListView):
    model = FutureStudentMembershipType
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_fut_mem(self.request)
        context['current_membership'] = str(current_membership.futuremembership)
        return context
    
    def post(self, request, **kwargs):
        selected_membership = request.POST.get('future_membership_type')
        fut_membership = get_user_fut_mem(request)
        fut_subscription = get_user_fut_subscription(request)
        
        selected_membership_qs = FutureStudentMembershipType.objects.filter(future_membership_type=selected_membership_type)
        
#        validation
        
        if fut_membership.futuremembership == selected_membership:
            if fut_subscription != None:
                messages.info(request, 'You already have this membership. Your next payment is die {}'.format('get this valeu from stripe'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        request.session['selected_membership_type'] = selected_membership.future_membership_type
        
        return HttpResponseRedirect(reverse('studentmemberships:paymentfuture'))