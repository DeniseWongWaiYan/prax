from django.contrib import admin

# Register your models here.
from .models import StudentMembership, FutureStudentMembershipType,  StudentFutureSubscription

admin.site.register(StudentMembership)
admin.site.register(FutureStudentMembershipType)
admin.site.register(StudentFutureSubscription)