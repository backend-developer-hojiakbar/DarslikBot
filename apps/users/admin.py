from django.contrib import admin
from .models import User, OneTimePassword
# Register your models here.
admin.site.register(User)


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ['otp']