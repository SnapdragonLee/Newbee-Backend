from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from models.basic.user import WXUser
from models.basic.notice import Notice
from models.basic.questions import Question, SubQuestion, Solution

from utils.defines import *


# Create your models here.

class ListOfQuestion(models.Model):
    openid = models.CharField(verbose_name='用户的openid', max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="对应的问题")

    def __str__(self):
        return self.openid

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e


class WrongQuestions(models.Model):
    openid = models.CharField(verbose_name='用户的openid', max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="对应的问题")
    date = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    havedone = models.BooleanField(verbose_name='是否已经做过', default=False, null=False)

    def __str__(self):
        return self.openid

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e


class history(models.Model):
    openid = models.CharField(verbose_name='用户的openid', max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="对应的问题")
    date = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    def __str__(self):
        return self.openid

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e


class UserApproveSolution(models.Model):
    class Type(models.IntegerChoices):
        LIKE = 1
        REPORT = 2

    user = models.ForeignKey(WXUser, on_delete=models.CASCADE, verbose_name='评价此题解的用户')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, verbose_name='被评价的题解')
    type = models.IntegerField(choices=Type.choices, verbose_name='用户评价此题解的类型')

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e


class done_question(models.Model):
    wxUser = models.ForeignKey(WXUser, on_delete=models.CASCADE, verbose_name='用户的openid')
    subQuestion = models.ForeignKey(SubQuestion, on_delete=models.CASCADE, verbose_name="对应的小题")
    option = models.CharField(verbose_name="用户选项", max_length=5,
                              choices=(('A', 'A'),
                                       ('B', 'B'),
                                       ('C', 'C'),
                                       ('D', 'D')), default='A')

    def __str__(self):
        return self.wxUser.id

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e
