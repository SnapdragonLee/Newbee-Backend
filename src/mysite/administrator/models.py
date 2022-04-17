from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from utils.defines import *


# Create your models here.
class Question(models.Model):
    id = models.AutoField(verbose_name='题目id', primary_key=True)
    title = models.TextField(verbose_name='题目标题',null=False)
    que_type = ((choice_que_name, '选择'),
                (cloze_que_name, '完形'),
                (reading_que_name, '阅读'))
    text = models.TextField(verbose_name='文章')
    sub_que_num = models.IntegerField(verbose_name='子问题数量', null=False)

    def __str__(self):
        return self.id

    # 每个模型类都必须有这个save函数
    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e

    class Meta:
        constraints = [
            models.CheckConstraint(check=(Q(que_type=choice_que_name) & Q(text__isnull=True)) | Q(text__isnull=False),
                                   name='check_text'),
            models.CheckConstraint(check=(Q(que_type=choice_que_name) & Q(sub_que_name=1)) | Q(sub_que_name__gte=1),
                                   name='check_sub_que_num'),

        ]


class SubQuestion(models.Model):
    id = models.AutoField(verbose_name='子问题id', primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="父问题的id")
    stem = models.TextField(verbose_name="子问题题干")
    A = models.TextField(null=False)
    B = models.TextField(null=False)
    C = models.TextField(null=False)
    D = models.TextField(null=False)
    answer = (('A', 'A'),
              ('B', 'B'),
              ('C', 'C'),
              ('D', 'D'))

    def __str__(self):
        return self.id

    # 每个模型类都必须有这个save函数
    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e

    class Meta:
        constraints = [
            models.CheckConstraint(check=(Q(question__type=cloze_que_name)&Q(stem__isnull=True))|Q(stem__isnull=False), name='check_stem'),

        ]
