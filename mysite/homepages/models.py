from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = ImageField(upload_to='users/%d/%m/%y', blank=True, null=True)
    #tutor
    #subscription english
    #subscription future school 
    
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
