from django.db import models
from django.urls import reverse
from django.conf import settings

from studentmemberships.models import FutureStudentMembershipType
from homepages.models import Group

# Create your models here.

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
    def futurelessons(self):
        return self.futurelesson_set.all().order_by('position')
    
class FutureLesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(FutureCourse, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    readinglist_url = models.CharField(max_length=200)
#    thumbnail = models.ImageField()
    description = models.TextField()
    assignment = models.TextField(blank=True)
    parentstips = models.TextField(blank=True)
    allowed_memberships = models.ManyToManyField(FutureStudentMembershipType)
    
    def __str__(self):
        return self.title
    
    def url(self):
        return reverse('courses:futurelessondetail', 
                       kwargs={
                           'course_slug': self.course.slug, 
                           'lesson_slug': self.slug })
    
class Forum(models.Model):
    topic= models.CharField(max_length=300)
    description = models.TextField(max_length=1000,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(FutureLesson, on_delete=models.SET_NULL, null=True)
    topicslug = models.SlugField(blank=True, null=True)
 
    def url(self):
        return reverse('courses:forum', 
                       kwargs={
                           'group_slug': self.group.slug, 
                           'lesson_slug': self.lesson.slug,
                           'topic_slug': self.topicslug
                       })
    
    def __str__(self):
        return str(self.topic)
    
class Discussion(models.Model):
    forum = models.ForeignKey(Forum, blank=True, null=True, on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    discuss = models.TextField()
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
 
    def __str__(self):
        return str(self.forum)

