from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    hwid = models.CharField(max_length=255, unique=True, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)


class Session(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
