from django.contrib import admin

# Register your models here.
from .models import EnglishTutor, FutureTutor

admin.site.register(EnglishTutor)
admin.site.register(FutureTutor)