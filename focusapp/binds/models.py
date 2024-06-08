from django.db import models
from focusapp.users.models import *


class Bind(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bind_name = models.CharField(max_length=255)
    script_path = models.CharField(max_length=255)
    key_binding = models.CharField(max_length=10)
