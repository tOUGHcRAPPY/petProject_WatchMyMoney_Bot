from django.db import models
from django.utils import timezone

from app.user.models import TelegramUser


class Finance(models.Model):
    description = models.CharField(max_length=200)
    finance_status = models.BooleanField(default=True)
    amount = models.FloatField(default=0)
    date_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(TelegramUser, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

