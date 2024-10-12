from django.contrib import admin

from apps.user.models import User, Privacy, Policy

admin.site.register(User)
admin.site.register(Policy)
admin.site.register(Privacy)
