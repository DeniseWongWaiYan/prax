from django.db import models
from django.conf import settings

# Create your models here.
class EnglishTutors(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField()
    videoslug = models.SlugField()
    qualifications = models.CharField(max_length=500, null=True)
    university = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class FutureTutors(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField()
    videoslug = models.SlugField()
    qualifications = models.CharField(max_length=500, null=True)
    university = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


