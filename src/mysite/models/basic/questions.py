from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.dispatch import receiver, Signal

from models.basic.user import WXUser
from utils.defines import CHOICE_QUE_NAME, CLOZE_QUE_NAME, READING_QUE_NAME


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
    bad_solution_num = models.IntegerField(verbose_name='该题目含有坏题解的数量', default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(bad_solution_num__gte=0), name='check_Question_bad_solution_num')
        ]

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

    # def add_bad_solution(self):
    #     self.bad_solution_num += 1
    #     self.save()
    #
    # def reduce_bad_solution(self):
    #     self.bad_solution_num -= 1
    #     self.save()

    def has_bad_solution(self, admin):
        sub_que_id_list = SubQuestion.objects.filter(question=self).values_list('id', flat=True)
        count = AdminApproveSolution.objects.filter(admin=admin, solution__is_bad=True,
                                                    solution__subQuestion_id__in=sub_que_id_list).count()

        return False if self.bad_solution_num == count else True


class SubQuestion(models.Model):
    # django默认字段参数中的null和blank都是false，所以以下写法很冗余
    id = models.AutoField(verbose_name='子问题id', primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="父问题的id")
    number = models.IntegerField(verbose_name='子问题题号')
    stem = models.TextField(verbose_name="子问题题干", null=True, blank=True)
    A = models.TextField(null=False)
    B = models.TextField(null=False)
    C = models.TextField(null=False)
    D = models.TextField(null=False)
    bad_solution_num = models.IntegerField(verbose_name='含有坏题解的数量', default=0)

    answer = models.CharField(verbose_name="答案", max_length=5,
                              choices=(('A', 'A'),
                                       ('B', 'B'),
                                       ('C', 'C'),
                                       ('D', 'D')), default='A')

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(bad_solution_num__gte=0), name='check_SubQuestion_bad_solution_num')
        ]

    def __str__(self):
        return 'id:' + str(self.id) + '   题干:' + str(self.stem)

    def clean(self):
        # 判断，完形题的小题题干为空，非完形题的小题题干不为空
        if not ((self.question.type == CLOZE_QUE_NAME and (self.stem is None or self.stem.strip().__len__() == 0)) or
                (self.question.type != CLOZE_QUE_NAME and self.stem is not None)):
            raise ValidationError

        # if self.bad_solution_num > Solution.objects.filter(subQuestion=self).count():
        #     raise ValidationError

        # if not (1 <= self.number <= self.question.sub_que_num):
        #     raise ValidationError

    # def reduce_bad_solution(self):
    #     self.bad_solution_num -= 1
    #     self.save()
    #     self.question.reduce_bad_solution()
    #
    # def add_bad_solution(self):
    #     self.bad_solution_num += 1
    #     self.save()
    #     self.question.add_bad_solution()

    def save(self, *args, **kwargs):
        try:
            if self.stem is not None and self.stem.strip().__len__() == 0:
                self.stem = None

            self.full_clean()
            super().save(*args, **kwargs)

        except ValidationError as e:
            raise e

    def has_bad_solution(self, admin):
        count = AdminApproveSolution.objects.filter(admin=admin, solution__is_bad=True,
                                                    solution__subQuestion=self).count()

        return False if count == self.bad_solution_num else True


class Solution(models.Model):
    id = models.AutoField(verbose_name='题解id', primary_key=True)
    subQuestion = models.ForeignKey(SubQuestion, on_delete=models.CASCADE, verbose_name="题解对应的子题目")
    wxUser = models.ForeignKey(WXUser, on_delete=models.CASCADE, verbose_name='发布此题解的用户')
    content = models.TextField(verbose_name='题解内容')
    likes = models.IntegerField(verbose_name='点赞数', default=0)
    reports = models.IntegerField(verbose_name='举报数', default=0)
    approval = models.IntegerField(verbose_name='被管理员认可的次数', default=0)
    is_bad = models.BooleanField(verbose_name='是否是坏题解', default=False)

    def __str__(self):
        return str(self.content)[0:20]

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(likes__gte=0), name='check_likes'),
            models.CheckConstraint(check=Q(reports__gte=0), name='check_reports'),
            models.CheckConstraint(check=Q(approval__gte=0), name='check_approval')
        ]

    def is_bad_solution(self):
        # self.refresh_from_db()
        return self.is_bad

    def set_bad_solution(self):
        if self.reports > 10 and ((self.reports - self.approval * 5) > self.likes * 2):
            self.is_bad = True
        else:
            self.is_bad = False

    def update_bad_solution(self):
        before = self.is_bad_solution()
        self.set_bad_solution()
        after = self.is_bad_solution()
        return before, after

    def positive_evaluation(self):
        before, after = self.update_bad_solution()
        if before and not after:
            modify_bad_solution_signal.send(sender=self.__class__, solution=self, cnt=-1)
            # self.subQuestion.reduce_bad_solution()

    def negative_evaluation(self):
        before, after = self.update_bad_solution()
        if not before and after:
            modify_bad_solution_signal.send(sender=self.__class__, solution=self, cnt=1)
            # self.subQuestion.add_bad_solution()

    def add_like(self):
        self.likes += 1
        self.positive_evaluation()
        self.wxUser.modify_likes(1)
        self.save()

    def add_report(self):
        self.reports += 1
        self.negative_evaluation()
        self.wxUser.modify_likes(-1)
        self.save()

    def add_approval(self):
        self.approval += 1
        self.positive_evaluation()
        self.save()

    def debug(self):
        before = self.is_bad_solution()
        self.set_bad_solution()
        after = self.is_bad_solution()
        if before and not after:
            modify_bad_solution_signal.send(sender=self.__class__, solution=self, cnt=-1)
        elif not before and after:
            modify_bad_solution_signal.send(sender=self.__class__, solution=self, cnt=1)

    def save(self, *args, **kwargs):
        try:
            # self.debug()
            # 如果用django管理器加举报数，则不要注释此行，正式版请把此行注释

            self.full_clean()
            super().save(*args, **kwargs)

        except ValidationError as e:
            raise e


modify_bad_solution_signal = Signal()


@receiver(modify_bad_solution_signal)
def modify_bad_solution_handler(sender, solution: Solution, cnt: int, **kwargs):
    sub_que_obj = solution.subQuestion
    sub_que_obj.bad_solution_num += cnt
    sub_que_obj.save()
    que_obj = sub_que_obj.question
    que_obj.bad_solution_num += cnt
    que_obj.save()


class AdminApproveSolution(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='认可该题解的管理员')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, verbose_name='被认可的题解')

    def __str__(self):
        return self.admin.username + " 确认了 id为" + str(self.solution.id) + " 的题解"

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e
