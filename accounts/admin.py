from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User

from accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(auth_admin.UserAdmin):
    inlines = (ProfileInline,)

# replace existing User admin form
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
