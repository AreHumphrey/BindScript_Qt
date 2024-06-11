# focusapp/subscriptions/models.py
from django.db import models
from focusapp.users.models import CustomUser
from django.utils import timezone


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_expired(self):
        return self.end_date < timezone.now()
