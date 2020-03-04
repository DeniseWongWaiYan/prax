from django.contrib import admin

# Register your models here.
from .models import EnglishCourse, EnglishLesson, FutureCourse, FutureLesson

admin.site.register(EnglishCourse)
admin.site.register(EnglishLesson)
admin.site.register(FutureCourse)
admin.site.register(FutureLesson)