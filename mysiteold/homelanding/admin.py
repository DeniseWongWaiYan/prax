from django.contrib import admin
from .models import StudentProfile, ParentProfile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','date_of_birth', 'profile_picture']

admin.site.register(StudentProfile, ProfileAdmin)

class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture']
admin.site.register(ParentProfile, ParentProfileAdmin)


