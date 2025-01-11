from django.contrib import admin

from .models import UserProfile, Group

admin.site.register(UserProfile)

admin.site.register(Group)

