from django.contrib import admin

# Register your models here.
from .models import ParentMembership, ParentMembershipType

admin.site.register(ParentMembership)
admin.site.register(ParentMembershipType)
