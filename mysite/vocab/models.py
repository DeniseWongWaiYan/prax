from django.db import models
from django.conf import settings

from studentmemberships.models import StudentMembership


# Create your models here.
class VocabularyWord(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    new_word = models.CharField(null=True, max_length=100)
    definition = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        template = '{0.student} {0.new_word}'
        return template.format(self)

