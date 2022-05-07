from enum import Enum

import django.utils.timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from utils.defines import *
from django.contrib.auth.models import User
import datetime


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

    def has_bad_solution(self):
        sub_que_set = SubQuestion.objects.filter(question=self)
        ret = False
        for sub_que in sub_que_set:
            if sub_que.has_bad_solution():
                ret = True
                break

        return ret


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
        return 'id:' + str(self.id) + '   题干:' + str(self.stem)

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

    def has_bad_solution(self):
        solution_set = Solution.objects.filter(subQuestion=self)
        ret = False
        for solution in solution_set:
            if solution.is_bad_solution():
                ret = True
                break
        return ret


class Solution(models.Model):
    id = models.AutoField(verbose_name='题解id', primary_key=True)
    subQuestion = models.ForeignKey(SubQuestion, on_delete=models.CASCADE, verbose_name="题解对应子题目的id")
    content = models.TextField(verbose_name='题解内容')
    likes = models.IntegerField(verbose_name='点赞数')
    reports = models.IntegerField(verbose_name='举报数')

    # bad_solution = models.BooleanField(verbose_name='是否被举报过多', default=False)

    def __str__(self):
        return str(self.content)[0:20]

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(likes__gte=0), name='check_likes'),
            models.CheckConstraint(check=Q(reports__gte=0), name='check_reports')
        ]

    def is_bad_solution(self):
        # self.refresh_from_db()
        if self.reports > 10 and (self.reports > self.likes * 3):
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e


class Notice(models.Model):
    time = models.DateTimeField(verbose_name='公告更新的时间', auto_now=True)
    content = models.TextField(verbose_name='公告内容', default='welcome to NewBee English')

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e


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
