from django.db import models


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=200)

    def __str__(self):
        return self.chat_id
