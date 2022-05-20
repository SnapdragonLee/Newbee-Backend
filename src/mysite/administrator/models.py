from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from models.basic.user import WXUser
from models.basic.questions import Question, SubQuestion, Solution
from utils.defines import *


# Create your models here.

class OperationRecord(models.Model):
    class OP_TYPE(models.TextChoices):
        ADD = '添加', '添加'
        MOD = '修改', '修改'
        DEL = '删除', '删除'
        OTHER = '其他', '其他'

    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='进行此操作的管理员')
    operation = models.CharField(verbose_name='操作类型', max_length=20,
                                 choices=OP_TYPE.choices,
                                 default=OP_TYPE.ADD)

    description = models.TextField(verbose_name='操作描述')
    time = models.DateTimeField(verbose_name='操作时间', auto_now=True)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e

    class Meta:
        ordering = ['-time']
