from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from datetime import datetime
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = ImageField(upload_to='users/%d/%m/%y', blank=True, null=True)
    id = models.IntegerField(null=False, primary_key=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = ImageField(upload_to='users/%d/%m/%y', blank=True, null=True)
    parent = models.ForeignKey(ParentProfile, on_delete=models.SET_NULL, null=True)
    #membershiptype = models.ForeignKey(StudentMembershipTypes, on_delete=models.SET_NULL, null=True)
    #subscription = models.ForeignKey(StudentSubscription, on_delete=models.SET_NULL, null=True)
    id = models.IntegerField(null=False, primary_key=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
