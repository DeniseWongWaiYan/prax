from django.contrib import admin

# Register your models here.
from .models import FutureGrades, FutureComment, FutCert

admin.site.register(FutureGrades)
admin.site.register(FutureComment)
admin.site.register(FutCert)