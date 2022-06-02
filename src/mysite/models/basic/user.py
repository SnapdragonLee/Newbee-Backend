from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class WXUser(models.Model):
    id = models.CharField(verbose_name='用户的openid', primary_key=True, max_length=50)
    user_name = models.CharField(verbose_name='用户名', max_length=20, null=False)
    total_choice = models.IntegerField(verbose_name='做过的选择题总数', default=0, null=False)
    right_choice = models.IntegerField(verbose_name='答对的选择题数', default=0, null=False)
    total_cloze = models.IntegerField(verbose_name='做过的完形小题总数', default=0, null=False)
    right_cloze = models.IntegerField(verbose_name='答对的完形小题数', default=0, null=False)
    total_reading = models.IntegerField(verbose_name='做过的阅读题小题总数', default=0, null=False)
    right_reading = models.IntegerField(verbose_name='做对的阅读题小题数', default=0, null=False)
    status = models.IntegerField(verbose_name="刷题阶段", default=0, null=False)
    solution_sum = models.IntegerField(verbose_name='用户发表的题解总数', default=0)
    likes = models.IntegerField(verbose_name='该用户发表的题解被点赞的总数', default=0)
    reports = models.IntegerField(verbose_name='该用户发表的题解被举报的总数', default=0)
    rank_question = models.IntegerField(verbose_name='该用户通过做题获得的积分排名', default=0)
    rank_solution = models.IntegerField(verbose_name='该用户通过写题解获得的积分', default=0)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e

    def modify_likes(self, variance: int):
        self.likes += variance
        self.save()

    def modify_reports(self, variance: int):
        self.reports += variance
        self.save()

    def add_solution_sum(self):
        self.solution_sum += 1
        self.save()

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(total_choice__gte=0), name='total_choice__gte_0'),
            models.CheckConstraint(check=Q(right_choice__gte=0), name='right_choice__gte_0'),
            models.CheckConstraint(check=Q(total_cloze__gte=0), name='total_cloze__gte_0'),
            models.CheckConstraint(check=Q(right_cloze__gte=0), name='right_cloze__gte_0'),
            models.CheckConstraint(check=Q(total_reading__gte=0), name='total_reading__gte_0'),
            models.CheckConstraint(check=Q(right_reading__gte=0), name='right_reading__gte_0'),
            models.CheckConstraint(check=Q(status__gte=0) & Q(status__lte=7), name='check_status')
        ]