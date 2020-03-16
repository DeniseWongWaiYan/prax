from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.generic import ListView, View

from .models import EnglishStudentMembershipType, FutureStudentMembershipType, StudentMembership, StudentEnglishSubscription, StudentFutureSubscription
 
import stripe 


from django.http import HttpResponse,StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import cv2
import time

def profile_view(request):
    user_eng = get_user_eng_mem(request)
    user_eng_sub = get_user_eng_subscription(request)
    user_future = get_user_fut_mem(request)
    user_future_sub = get_user_future_subscription(request)
    
    context = {
        'user_eng': user_eng,
        'user_eng_sub': user_eng_sub,
        'user_future': user_future,
        'user_future_sub': user_future_sub
        
    }
    
    return render(request, "studentmemberships/profile.html", context)


def get_user_eng_mem(request):
    eng_mem_qs = StudentMembership.objects.filter(user=request.user)
    if eng_mem_qs.exists():
        return eng_mem_qs.first()
#    return None

def get_user_eng_subscription(request):
    user_sub_qs = StudentEnglishSubscription.objects.filter(englishmembershiptype=get_user_eng_mem(request))
    
    if user_sub_qs.exists():
        user_sub_qs = user_sub_qs.first()
        return user_sub_qs
#    return None

def get_sel_eng_mem(request):
    membership_type =  request.session['selected_eng_membership_type']
    print(request.session['selected_eng_membership_type'])
    selected_mem_qs = EnglishStudentMembershipType.objects.filter(english_membership_type = membership_type)
    if selected_mem_qs.exists():
        return selected_mem_qs.first()
    return None

def get_user_fut_mem(request):
    fut_mem_qs = StudentMembership.objects.filter(user=request.user)
    if fut_mem_qs.exists():
        return fut_mem_qs.first()
    return None


class StudentEnglishMembershipSelectView(ListView):
    model = EnglishStudentMembershipType
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_eng_mem(self.request)
        context['current_membership'] = str(current_membership.englishmembership)
        return context

    def post(self, request, **kwargs):
        eng_membership = get_user_eng_mem(request)
        eng_subscription = get_user_eng_subscription(request)
        selected_membership_type = request.POST.get('english_membership_type')
        
        selected_membership = EnglishStudentMembershipType.objects.get(english_membership_type=selected_membership_type)
    
        #        validation
        if eng_membership.englishmembership == selected_membership:
            if eng_subscription != None:
                messages.info(request, 'You already have this membership. Your next payment is die {}'.format('get this value from stripe'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        #assign
        
        request.session['selected_eng_membership_type'] = selected_membership.english_membership_type
        print(request.session['selected_eng_membership_type'])
        
        
        return HttpResponseRedirect(reverse('studentmemberships:engpay'))

    
def EngPaymentView(request):    
    eng_mem = get_user_eng_mem(request)
    eng_sel_mem = get_sel_eng_mem(request)
    
    
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    

    if request.method == "POST":
                        
            customer = stripe.Customer.retrieve(eng_mem.stripe_customer_id)
            token = request.POST['stripeToken']
            
            customer.source = token # 4242424242424242
            customer.save()
            
            
            subscription = stripe.Subscription.create(
                customer=eng_mem.stripe_customer_id,
                items=[
                    { "plan": eng_sel_mem.stripe_plan_id },
                ]
            )
                
            return redirect(reverse('studentmemberships:updatetransactioneng',
                           kwargs={'subscription_id': subscription.id }))
            
        
        
            # messages.info(request, "Your card has been declined." )

    context = {
        'publishKey': publishKey,
        'selected_membership': eng_sel_mem,
    }
    return render(request, 'studentmemberships/studentengpay.html', context)

    # return render(request, 'studentmemberships/studentengpay.html', context)

def updateEngTransaction(request, subscription_id):
    eng_mem = get_user_eng_mem(request)
    eng_sel_mem = get_sel_eng_mem(request)
    
    eng_mem.englishmembership = eng_sel_mem
    eng_mem.save()
    
    sub, created = StudentEnglishSubscription.objects.get_or_create(englishmembershiptype=eng_mem)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()
    
    try:
        del request.session['selected_eng_membership_type']
    except:
        pass
    
    messages.info(request, "succesfully created {} membership".format(eng_sel_mem))
    
    return redirect('/courses/english')

def get_user_future_subscription(request):
    user_sub_qs = StudentFutureSubscription.objects.filter(futuremembershiptype=get_user_fut_mem(request))
    
    if user_sub_qs.exists():
        user_sub_qs = user_sub_qs.first()
        return user_sub_qs
    return None

class StudentFutureMembershipSelectView(ListView):
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
                messages.info(request, 'You already have this membership. Your next payment is die {}'.format('get this valeu from stripe'))
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


def get_frame():
    camera =cv2.VideoCapture(0) 
    while True:
        _, img = camera.read()
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    del(camera)
    
def indexscreen(request, videoslug): 
     student = StudentMembership.objects.get(user=request.user)
     videoslug = student.videoslug

     context = {
        'videoslug': videoslug,
     }

     return render(request, "tutors/screens.html", context)
    # try:
    #   template = "screens.html"
    #   return render(request, template)
    # except:
    #     pass

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"

