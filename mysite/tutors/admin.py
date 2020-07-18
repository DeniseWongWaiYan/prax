from django.contrib import admin

# Register your models here.
from .models import EnglishTutors, FutureTutors

admin.site.register(EnglishTutors)
admin.site.register(FutureTutors)