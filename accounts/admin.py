from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import LLDUser

admin.site.register(LLDUser, UserAdmin)
