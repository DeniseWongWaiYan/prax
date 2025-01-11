from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from homepages.models import UserProfile
import datetime

import stripe 

# Create your models here.

PARENT_MEMBERSHIP_CHOICES = (
    ('Smile School Parents', 'Parent'),
    ('No Smile School Parents', 'Parent No')
)

class ParentMembershipType(models.Model):
    slug = models.SlugField()
    parent_membership_type = models.CharField(choices=PARENT_MEMBERSHIP_CHOICES, default='No Smile School Parents', max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.parent_membership_type

class ParentMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    parentmembership = models.ForeignKey(
    ParentMembershipType, on_delete=models.SET_NULL, null=True)   

    def __str__(self):
        return self.user.username
    

def post_save_parentmembership_create(sender, instance, created, *args, **kwargs):
    if created:
        ParentMembership.objects.get_or_create(user=instance)
        
    parent_membership, created = ParentMembership.objects.get_or_create(user=instance)
    
    if parent_membership.stripe_customer_id is None or parent_membership.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        parent_membership.stripe_customer_id = new_customer_id['id']
        parent_membership.save()

post_save.connect(post_save_parentmembership_create, sender=settings.AUTH_USER_MODEL)

class ParentSubscription(models.Model):
    parentmembershiptype = models.ForeignKey(ParentMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.parentmembershiptype.user.username
    
    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.datetime.fromtimestamp(subscription.created)
    
    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
        return datetime.datetime.fromtimestamp(subscription.current_period_end)
