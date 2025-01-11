from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from tutors.models import FutureTutor
from grades.models import FutureComment
from homepages.models import UserProfile
from grades.models import FutureGrades
from django.db.models import Avg, Count
from courses.models import Discussion

from homepages.models import Group

import json

from django.views.generic import ListView, View

from .models import FutureStudentMembershipType, StudentMembership, StudentFutureSubscription
 
import stripe 

from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
#import cv2
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def rank(request):
    futgrades = FutureGrades.objects.filter(student = request.user).all()
    discuss = Discussion.objects.filter(student=request.user)

    points = int(futgrades.count()) + int(discuss.count())
    
    rank = "none yet"
    left = 0
    if points  == 0:
        rank = "Novice"
    elif 0 < points <= 5:
        rank = "Youngling"
        left = 5-points
    elif 5 < points <= 10:
        rank = "Senior Youngling"
        left = 10-points
    elif 10 < points <= 20:
        rank = "Junior Padawan"
        left = 20-points
    elif 20 < points <= 35:
        rank = "Padawan"
        left = 35-points
    elif 40 < points <= 52:
        rank = "Senior Padawan"
        left = 70-points
    elif 70 < points <= 60:
        rank = "Jedi"
        left = 100-points
    else:
        rank = "Jedi Knight"
        
    context = {
        'points': points,
        'rank': rank,
        'left': left, 
     }
    
    return(context)


@login_required
def profile_view(request):
    user_future = get_user_fut_mem(request)
    user_future_sub = get_user_future_subscription(request)
    fut_comment = FutureComment.objects.filter(student=request.user).last()
    refcode = str(request.user.id)+'ref'+str(request.user)
    referred = UserProfile.objects.filter(referredby=refcode).count() 
    
    
    students_in_group = StudentMembership.objects.filter(group=request.user.studentmembership.group).exclude(user=request.user)
    
    rank1 = rank(request)
    
    context = {
        'user_future': user_future,
        'user_future_sub': user_future_sub,
        'fut_comment': fut_comment,
        'refcode': refcode,
        'referred': referred,
        'points': rank1['points'],
        'rank': rank1['rank'],
        'left': rank1['left'],
        'students_in_group': students_in_group,
    }
    
    return render(request, "studentmemberships/profile.html", context)


def get_user_fut_mem(request):
    fut_mem_qs = StudentMembership.objects.filter(user=request.user)
    if fut_mem_qs.exists():
        return fut_mem_qs.first()
    return None



def get_user_future_subscription(request):
    user_sub_qs = StudentFutureSubscription.objects.filter(futuremembershiptype=get_user_fut_mem(request))
    
    if user_sub_qs.exists():
        user_sub_qs = user_sub_qs.first()
        return user_sub_qs
    return None

class StudentFutureMembershipSelectView(LoginRequiredMixin, ListView):
    model = FutureStudentMembershipType
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_fut_mem(self.request)
        context['current_membership'] = str(current_membership.futuremembership)
        return context
    
    def post(self, request, **kwargs):
        fut_membership = get_user_fut_mem(request)
        fut_subscription = get_user_future_subscription(request)
        selected_membership_type = request.POST.get('future_membership_type')
        
        selected_membership = FutureStudentMembershipType.objects.get(future_membership_type=selected_membership_type)
        

#        validation
        
        if fut_membership.futuremembership == selected_membership:
            if fut_subscription != None:
                messages.info(request, 'You already have this membership. Your next payment is die {}'.format('get this value from stripe'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        request.session['selected_future_membership'] = selected_membership.future_membership_type

        return HttpResponseRedirect(reverse('studentmemberships:futurepay'))

def get_sel_fut_mem(request):
    membership_type = request.session['selected_future_membership']
    #    FutureStudentMembershipType.objects.get(future_membership_type=request.POST.get('future_membership_type'))
    selected_mem_qs = FutureStudentMembershipType.objects.filter(future_membership_type = membership_type)
    if selected_mem_qs.exists():
        return selected_mem_qs.first()
    return None

@login_required
def FutPaymentView(request):    
    fut_mem = get_user_fut_mem(request)
    fut_sel_mem = get_sel_fut_mem(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    
    if request.method == "POST":
        
            customer = stripe.Customer.retrieve(fut_mem.stripe_customer_id)
            
            customer.source = request.POST['stripeToken'] # 4242424242424242
            
            customer.save()
                        
            subscription = stripe.Subscription.create(
                customer=fut_mem.stripe_customer_id,
                items=[
                    { "plan": fut_sel_mem.stripe_plan_id },
                ]
            )
            return redirect(reverse('studentmemberships:updatetransactionfut',
                           kwargs={'subscription_id': subscription.id }))

            
    context = {
        'publishKey': publishKey,
        'selected_membership': fut_sel_mem,
    }
    
    return render(request, 'studentmemberships/studentfutpay.html', context)

def updateFutTransaction(request, subscription_id):
    fut_mem = get_user_fut_mem(request)
    fut_sel_mem = get_sel_fut_mem(request)
    
    fut_mem.futuremembership = fut_sel_mem
    fut_mem.save()
    
    sub, created = StudentFutureSubscription.objects.get_or_create(futuremembershiptype=fut_mem)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()
    
    try:
        del request.session['selected_future_membership']
    except:
        pass
    
    messages.info(request, "succesfully created {} membership".format(fut_sel_mem))
    
    return redirect('/courses/future')


def indexscreen(request, videoslug): 
     student = StudentMembership.objects.get(user=request.user)
     videoslug = student.videoslug

     context = {
        'videoslug': videoslug,
     }

     return render(request, "studentmemberships/screens.html", context)

