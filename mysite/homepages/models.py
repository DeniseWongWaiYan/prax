from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField

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
    #tutor
    #subscription english
    #subscription future school 
    
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
