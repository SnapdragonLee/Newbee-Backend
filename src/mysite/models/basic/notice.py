from django.core.exceptions import ValidationError
from django.db import models


class Notice(models.Model):
    time = models.DateTimeField(verbose_name='公告更新的时间', auto_now=True)
    content = models.TextField(verbose_name='公告内容', default='welcome to NewBee English')

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e
