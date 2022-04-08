from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

class AdminTable(models.Model):
    user_name = models.CharField(verbose_name='管理员账号名', primary_key=True, max_length=20)
    password = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e


class UserTable(models.Model):
    id = models.CharField(verbose_name='用户的openid', primary_key=True, max_length=30)
    user_name = models.CharField(verbose_name='用户名', unique=True, max_length=20, null=False)
    recent_choice_que = models.IntegerField(verbose_name='近期答对选择题数', default=0)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e

    class Meta:
        constraints = [
            models.CheckConstraint()
        ]
