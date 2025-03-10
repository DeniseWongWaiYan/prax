from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
import datetime
from tutors.models import EnglishTutor, FutureTutor, IGCSETutor
from homepages.models import Group

import stripe

#from django.utils.translation import gettext as _

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.


STUDENT_FUTURE_MEMBERSHIP_CHOICES = (
    ('Smile School Future Full', 'Future Full'),
    ('Smile School Future Basic', 'Future Basic'),
    ('No Smile School Future', 'Future No')
)

    
class FutureStudentMembershipType(models.Model):
    slug = models.SlugField()
    future_membership_type = models.CharField(choices=STUDENT_FUTURE_MEMBERSHIP_CHOICES, default='No Smile School Future', max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)
    description = models.TextField(null=True)

    def __str__(self):
        return self.future_membership_type

    
class StudentMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    futuremembership = models.ForeignKey(
        FutureStudentMembershipType, on_delete=models.SET_NULL, null=True)
    futuretutor = models.ForeignKey(
        FutureTutor, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.user.username

def post_save_studentmembership_create(sender, instance, created, *args, **kwargs):
    if created:
        StudentMembership.objects.get_or_create(user=instance)
        
    student_membership, created = StudentMembership.objects.get_or_create(user=instance)
    
    if student_membership.stripe_customer_id is None or student_membership.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        student_membership.stripe_customer_id = new_customer_id['id']
        student_membership.save()

post_save.connect(post_save_studentmembership_create, sender=settings.AUTH_USER_MODEL)
    
class StudentEnglishSubscription(models.Model):
    englishmembershiptype = models.ForeignKey(StudentMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.englishmembershiptype.user.username
    
    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.datetime.fromtimestamp(subscription.created)
    
    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.datetime.fromtimestamp(subscription.current_period_end)
    
    @property
    def get_begin_billing_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.datetime.fromtimestamp(subscription.current_period_start)
        
class StudentFutureSubscription(models.Model):
    futuremembershiptype = models.ForeignKey(StudentMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.futuremembershiptype.user.username

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.datetime.fromtimestamp(subscription.created)
    
    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.datetime.fromtimestamp(subscription.current_period_end)
    
    @property
    def get_begin_billing_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.datetime.fromtimestamp(subscription.current_period_start)
    