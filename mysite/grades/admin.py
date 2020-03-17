from django.contrib import admin

# Register your models here.
from .models import EnglishGrades, FutureGrades

admin.site.register(EnglishGrades)
admin.site.register(FutureGrades)