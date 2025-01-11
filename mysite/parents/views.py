from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Avg

from django.views.generic import ListView, View

from studentmemberships.models import StudentMembership
from .models import ParentMembershipType, ParentMembership, ParentSubscription 
from grades.models import EnglishGrades, FutureGrades, FutCert
from grades.views import grades

import stripe 


from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
import time

def profile_view(request):
    parent_mem = get_parent_mem(request)
    parent_sub = get_parent_subscription(request)
    parent = ParentMembership.objects.filter(user=request.user)
    children = StudentMembership.objects.filter(parents__in=parent).all()
    
    futgrades = []
#    futgrades = [[] for i in range(children.count())]
    certs = []
    creativity = []
    critical_thinking = []
    communication = []
    collaboration = []
    leadership = []
    social_cultural_awareness = []
    
    for child in children:
        futgrades.extend(FutureGrades.objects.filter(student = child.user).all())
        certs.append(FutCert.objects.filter(student=child.user).all())

        creativity.append(FutureGrades.objects.filter(student = child.user).aggregate(Avg('creativity'))['creativity__avg'])

        critical_thinking.append(FutureGrades.objects.filter(student = child.user).aggregate(Avg('critical_thinking'))['critical_thinking__avg'])

        communication.append(FutureGrades.objects.filter(student = child.user).aggregate(Avg('communication'))['communication__avg'])

        collaboration.append(FutureGrades.objects.filter(student = child.user).aggregate(Avg('collaboration'))['collaboration__avg'])

        leadership.append(FutureGrades.objects.filter(student = child.user).aggregate(Avg('leadership'))['leadership__avg'])
        
        social_cultural_awareness.append(FutureGrades.objects.filter(student = child.user).aggregate(Avg('social_cultural_awareness'))['social_cultural_awareness__avg'])

    avgcreativity = FutureGrades.objects.all().aggregate(Avg('creativity'))['creativity__avg']

    avgct = FutureGrades.objects.all().aggregate(Avg('critical_thinking'))['critical_thinking__avg']

    
    avcomm = FutureGrades.objects.all().aggregate(Avg('communication'))['communication__avg']

    avcollab = FutureGrades.objects.all().aggregate(Avg('collaboration'))['collaboration__avg']

    avlead = FutureGrades.objects.all().aggregate(Avg('leadership'))['leadership__avg']

    avaware = FutureGrades.objects.all().aggregate(Avg('social_cultural_awareness'))['social_cultural_awareness__avg']
    
    
    context = {
    'parent_mem': parent_mem,
    'parent_sub': parent_sub,
    'children': children,
    'futuregrades': futgrades,
    'creativity': creativity,
    'critical_thinking': critical_thinking,
    'communication': communication,
    'collaboration': collaboration,
    'leadership': leadership,
    'social_cultural_awareness': social_cultural_awareness,
    'avgcreativity': avgcreativity,
    'avgct':avgct, 
    'avcomm':avcomm,
    'avcollab':avcollab,
    'avlead':avlead,
    'avaware': avaware,
    'certs': certs,
    
    }
    
    return render(request, "parents/profile.html", context)


def get_parent_mem(request):
    parent_mem_qs = ParentMembership.objects.filter(user=request.user)
    if parent_mem_qs.exists():
        return parent_mem_qs.first()
#    return None

def get_parent_subscription(request):
    user_sub_qs = ParentSubscription.objects.filter(parentmembershiptype=get_parent_mem(request))
    
    if user_sub_qs.exists():
        user_sub_qs = user_sub_qs.first()
        return user_sub_qs
#    return None

def get_sel_parent_mem(request):
    membership_type =  request.session['selected_parent_membership_type']
    
    selected_mem_qs = ParentMembershipType.objects.filter(parent_membership_type = membership_type)
    if selected_mem_qs.exists():
        return selected_mem_qs.first()
    return None


class ParentMembershipSelectView(ListView):
    model = ParentMembershipType
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_parent_mem(self.request)
        context['current_membership'] = str(current_membership.parentmembership)
        return context

    def post(self, request, **kwargs):
        parent_mem = get_parent_mem(request)
        parent_sub = get_parent_subscription(request)
        selected_membership_type = request.POST.get('parent_membership_type')
        
        selected_membership = ParentMembershipType.objects.get(parent_membership_type=selected_membership_type)
    
        #        validation
        if parent_mem.parentmembership == selected_membership:
            if parent_sub != None:
                messages.info(request, 'You already have this membership. Your next payment is die {}'.format('get this value from stripe'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        #assign
        
        request.session['selected_parent_membership_type'] = selected_membership.parent_membership_type
     
        
        
        return HttpResponseRedirect(reverse('parents:parentpay'))

    
def ParentPaymentView(request):    
    parent_mem = get_parent_mem(request)
    parent_sel_mem = get_sel_parent_mem(request)
    
    
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    

    if request.method == "POST":
                        
            customer = stripe.Customer.retrieve(parent_mem.stripe_customer_id)
            token = request.POST['stripeToken']
            
            customer.source = token # 4242424242424242
            customer.save()
            
            
            subscription = stripe.Subscription.create(
                customer=parent_mem.stripe_customer_id,
                items=[
                    { "plan": parent_sel_mem.stripe_plan_id },
                ]
            )
                
            return redirect(reverse('prents:updatetransaction',
                           kwargs={'subscription_id': subscription.id }))
            
        
        
            # messages.info(request, "Your card has been declined." )

    context = {
        'publishKey': publishKey,
        'selected_membership': parent_sel_mem,
    }
    return render(request, 'parents/parentpay.html', context)

    # return render(request, 'studentmemberships/studentengpay.html', context)

def updateTransaction(request, subscription_id):
    parent_mem = get_parent_mem(request)
    parent_sel_mem = get_sel_parent_mem(request)
    
    parent_mem.parentmembership = parent_sel_mem
    parent_mem.save()
    
    sub, created = ParentSubscription.objects.get_or_create(parentmembershiptype=parent_mem)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()
    
    try:
        del request.session['selected_parent_membership_type']
    except:
        pass
    
    messages.info(request, "succesfully created {} membership".format(parent_sel_mem))
    
    return redirect('/courses/')
