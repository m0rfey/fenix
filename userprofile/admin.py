from django.contrib import admin

from userprofile.models import User


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        fields = ['avatar']

admin.site.register(User, UserAdmin)
