from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }


class OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)


    def __str__(self):
        return f"{self.user.first_name} - otp code"


class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Pupil(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.first_name)