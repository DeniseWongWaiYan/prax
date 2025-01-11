from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField
from tutors.models import EnglishTutor, FutureTutor, IGCSETutor



USERTYPE_CHOICES = (
    ('Parent', 'Parent'),
    ('Child', 'Child'),
    ('None', 'None'),
)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = ImageField(upload_to='users/%d/%m/%y', blank=True, null=True)
    usertype = models.CharField(choices=USERTYPE_CHOICES, default='None', max_length=30)
    referredby = models.CharField(blank=True, null=True, max_length=30)
    #tutor
    #subscription english
    #subscription future school 
    
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class Group(models.Model):
    name = models.CharField(blank=True, null=True, max_length=30)
    slug = models.SlugField(blank=True, null=True, max_length=30)
    next_lesson = models.DateField(blank=True, null=True)
    futuretutor = models.ForeignKey(
        FutureTutor, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name
