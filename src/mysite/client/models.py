from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, UserManager
from django.db.models import Q


# Create your models here.

class WXUser(models.Model):
    id = models.CharField(verbose_name='用户的openid', primary_key=True, max_length=50)
    user_name = models.CharField(verbose_name='用户名', max_length=20, null=False)
    recent_choice = models.IntegerField(verbose_name='近期答对选择题数', default=0, null=False)
    recent_cloze = models.IntegerField(verbose_name='近期答对完形小题数', default=0, null=False)
    recent_reading = models.IntegerField(verbose_name='近期答对阅读小题数', default=0, null=False)
    total_choice = models.IntegerField(verbose_name='做过的选择题总数', default=0, null=False)
    right_choice = models.IntegerField(verbose_name='答对的选择题数', default=0, null=False)
    total_cloze = models.IntegerField(verbose_name='做过的完形小题总数', default=0, null=False)
    right_cloze = models.IntegerField(verbose_name='答对的完形小题数', default=0, null=False)
    total_reading = models.IntegerField(verbose_name='做过的阅读题小题总数', default=0, null=False)
    right_reading = models.IntegerField(verbose_name='做对的阅读题小题数', default=0, null=False)
    status = models.IntegerField(verbose_name="刷题阶段", default=0, null=False)

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(recent_choice__gte=0), name='recent_choice__gte_0'),
            models.CheckConstraint(check=Q(recent_cloze__gte=0), name='recent_cloze__gte_0'),
            models.CheckConstraint(check=Q(recent_reading__gte=0), name='recent_reading__gte_0'),
            models.CheckConstraint(check=Q(total_choice__gte=0), name='total_choice__gte_0'),
            models.CheckConstraint(check=Q(right_choice__gte=0), name='right_choice__gte_0'),
            models.CheckConstraint(check=Q(total_cloze__gte=0), name='total_cloze__gte_0'),
            models.CheckConstraint(check=Q(right_cloze__gte=0), name='right_cloze__gte_0'),
            models.CheckConstraint(check=Q(total_reading__gte=0), name='total_reading__gte_0'),
            models.CheckConstraint(check=Q(right_reading__gte=0), name='right_reading__gte_0'),
            models.CheckConstraint(check=Q(status=0) | Q(status=1), name='check_status')
        ]
