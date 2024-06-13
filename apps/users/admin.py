from django.contrib import admin
from .models import User, OneTimePassword, Status, Type, Pupil
# Register your models here.
admin.site.register(User)


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ['otp']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'type']
    list_filter = ['status', 'type']