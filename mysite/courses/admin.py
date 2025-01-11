from django.contrib import admin

# Register your models here.
from .models import FutureCourse, FutureLesson, Forum, Discussion

admin.site.register(FutureCourse)
admin.site.register(Forum)
admin.site.register(Discussion)
admin.site.register(FutureLesson)
