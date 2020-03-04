from django.contrib import admin

# Register your models here.
from .models import StudentMembership, EnglishStudentMembershipType,  FutureStudentMembershipType, StudentEnglishSubscription, StudentFutureSubscription 

admin.site.register(StudentMembership)
admin.site.register(EnglishStudentMembershipType)
admin.site.register(FutureStudentMembershipType)
admin.site.register(StudentEnglishSubscription)
admin.site.register(StudentFutureSubscription)