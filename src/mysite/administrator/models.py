from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from utils.defines import *


# Create your models here.
class Question(models.Model):
    id = models.AutoField(verbose_name='题目id', primary_key=True)
    title = models.TextField(verbose_name='题目标题', null=False)
    que_type = models.CharField(verbose_name='题目类型', max_length=20,
                                choices=(
                                    (choice_que_name, '选择'),
                                    (cloze_que_name, '完形'),
                                    (reading_que_name, '阅读')
                                ), default=choice_que_name)

    text = models.TextField(verbose_name='文章', null=True, blank=True)
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
            models.CheckConstraint(check=(Q(que_type=choice_que_name) & Q(sub_que_num=1)) | Q(sub_que_num__gte=1),
                                   name='check_sub_que_num'),

        ]


# django默认字段参数中的null和blank都是false，所以以下写法很冗余
class SubQuestion(models.Model):
    id = models.AutoField(verbose_name='子问题id', primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="父问题的id")
    stem = models.TextField(verbose_name="子问题题干", null=True, blank=True)
    A = models.TextField(null=False)
    B = models.TextField(null=False)
    C = models.TextField(null=False)
    D = models.TextField(null=False)

    answer = models.CharField(verbose_name="答案", max_length=5,
                              choices=(('A', 'A'),
                                       ('B', 'B'),
                                       ('C', 'C'),
                                       ('D', 'D')), default='A')

    def __str__(self):
        return self.id

    # 每个模型类都必须有这个save函数
    def save(self, *args, **kwargs):
        try:
            # 先判断，完形题的小题题干为空，非完形题的小题题干不为空
            if not ((self.question.que_type == cloze_que_name and self.stem is None) or (self.stem is not None)):
                raise ValidationError
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e

    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=(Q(question__que_type=cloze_que_name) & Q(stem__isnull=True)) | Q(stem__isnull=False),
    #             name='check_stem'),
    #
    #     ]
