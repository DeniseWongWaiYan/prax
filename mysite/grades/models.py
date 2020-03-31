from django.db import models
from django.conf import settings

from studentmemberships.models import StudentMembership
from courses.models import EnglishLesson, FutureLesson
# Create your models here.

def user_directory_path(instance, filename):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    return 'user_{0}/{1}'.format(student, filename)

class EnglishGrades(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    lesson = models.ForeignKey(EnglishLesson, on_delete=models.DO_NOTHING)
    upload = models.FileField(upload_to='user_directory_path', blank=True)
    upload_corrected = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True)
    vocab = models.IntegerField(null=True)
    grammar = models.IntegerField(null=True)
    content = models.IntegerField(null=True)
    creativity = models.IntegerField(null=True)
    comments = models.TextField(null=True)
    
    def __str__(self):
        template = '{0.student} {0.lesson}'
        return template.format(self)

class FutureGrades(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    lesson = models.ForeignKey(FutureLesson, on_delete=models.DO_NOTHING)
    vocab = models.IntegerField()
    grammar = models.IntegerField()
    content = models.IntegerField()
    creativity = models.IntegerField()
    
    def __str__(self):
        template = '{0.student} {0.lesson}'
        return template.format(self)