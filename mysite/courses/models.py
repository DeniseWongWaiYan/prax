from django.db import models

from studentmemberships.models import EnglishStudentMembershipType, FutureStudentMembershipType

# Create your models here.
class EnglishCourse(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(EnglishStudentMembershipType)
    
    def __str__(self):
        return self.title
    
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