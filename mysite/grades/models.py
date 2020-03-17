from django.db import models
from django.conf import settings

from studentmemberships.models import StudentMembership
from courses.models import EnglishLesson, FutureLesson
# Create your models here.
class EnglishGrades(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    lesson = models.ForeignKey(EnglishLesson, on_delete=models.DO_NOTHING)
    vocab = models.IntegerField()
    grammar = models.IntegerField()
    content = models.IntegerField()
    creativity = models.IntegerField()
    
    def __str__(self):
        template = '{0.student} {0.lesson}'
        return template.format(self)

class FutureGrades(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    lesson = models.ForeignKey(FutureLesson, on_delete=models.DO_NOTHING)
    vocab = models.IntegerField()
    grammar = models.IntegerField()
    content = models.IntegerField()
    creativity = models.IntegerField()
    
    def __str__(self):
        return str(self.student.user), str(self.lesson) 