from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from utils.defines import *


# Create your models here.
class Question(models.Model):
    id = models.AutoField(verbose_name='题目id', primary_key=True)
    title = models.TextField(verbose_name='题目标题', null=False)

    type = models.CharField(verbose_name='题目类型', max_length=20,
                            choices=(
                                (CHOICE_QUE_NAME, '选择'),
                                (CLOZE_QUE_NAME, '完形'),
                                (READING_QUE_NAME, '阅读')
                            ), default=CHOICE_QUE_NAME
                            )

    text = models.TextField(verbose_name='文章', null=True, blank=True)
    sub_que_num = models.IntegerField(verbose_name='子问题数量', null=False)

    def __str__(self):
        return self.title

    def clean(self):
        if not ((self.type == CHOICE_QUE_NAME and (self.text is None or self.text.strip().__len__() == 0)) or
                (self.type != CHOICE_QUE_NAME and self.text is not None)):
            raise ValidationError

        if not ((self.type == CHOICE_QUE_NAME and self.sub_que_num == 1) or (
                self.type != CHOICE_QUE_NAME and self.sub_que_num >= 1)):
            raise ValidationError

    def save(self, *args, **kwargs):
        try:
            if self.text is not None and self.text.strip().__len__() == 0:
                self.text = None

            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e


# django默认字段参数中的null和blank都是false，所以以下写法很冗余
class SubQuestion(models.Model):
    id = models.AutoField(verbose_name='子问题id', primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="父问题的id")
    number = models.IntegerField(verbose_name='子问题题号')
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
        return 'id:' + str(self.id) + '   题干:' + self.stem

    def clean(self):
        # 判断，完形题的小题题干为空，非完形题的小题题干不为空
        if not ((self.question.type == CLOZE_QUE_NAME and (self.stem is None or self.stem.strip().__len__() == 0)) or
                (self.question.type != CLOZE_QUE_NAME and self.stem is not None)):
            raise ValidationError

        if not (1 <= self.number <= self.question.sub_que_num):
            raise ValidationError

    def save(self, *args, **kwargs):
        try:
            if self.stem is not None and self.stem.strip().__len__() == 0:
                self.stem = None

            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e
