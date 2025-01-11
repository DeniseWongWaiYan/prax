from django.db import models
from django.conf import settings

from studentmemberships.models import StudentMembership
from courses.models import FutureLesson
# Create your models here.

def user_directory_path(instance, filename):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    return 'user_{0}/{1}'.format(student, filename)

class FutureGrades(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    lesson = models.ForeignKey(FutureLesson, on_delete=models.DO_NOTHING)
    critical_thinking = models.IntegerField(null=True)
    creativity = models.IntegerField(null=True)
    communication = models.IntegerField(null=True)
    collaboration = models.IntegerField(null=True)
    
    
    def __str__(self):
        template = '{0.student} {0.lesson}'
        return template.format(self)
    
class FutureComment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    comments = models.TextField(null=True)
    date = models.DateTimeField(null=True)

    
    def __str__(self):
        template = '{0.student} {0.comments}'
        return template.format(self)
    
class FutCert(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    cert = models.TextField(null=True)
    date = models.DateTimeField(null=True)

    
    def __str__(self):
        template = '{0.student} {0.cert}'
        return template.format(self)