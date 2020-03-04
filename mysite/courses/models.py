from django.db import models
from django.urls import reverse

from studentmemberships.models import EnglishStudentMembershipType, FutureStudentMembershipType

# Create your models here.
class EnglishCourse(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(EnglishStudentMembershipType)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:englishdetail', kwargs={'slug': self.slug})
    
    @property 
    def englishlesson(self):
        return self.englishlesson_set.all().order_by('position')
    
class EnglishLesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(EnglishCourse, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    readinglist_url = models.CharField(max_length=200)
    thumbnail = models.ImageField()
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(EnglishStudentMembershipType)
    
    def __str__(self):
        return self.title

class FutureCourse(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(FutureStudentMembershipType)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:futuredetail', kwargs={'slug': self.slug})
    
    @property 
    def futurelesson(self):
        return self.futurelesson_set.all().order_by('position')
    
class FutureLesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(FutureCourse, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    readinglist_url = models.CharField(max_length=200)
    thumbnail = models.ImageField()
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(FutureStudentMembershipType)
    
    def __str__(self):
        return self.title