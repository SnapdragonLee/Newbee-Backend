from rest_framework import serializers
from .models import Question, SubQuestion, Solution, OperationRecord, AdminApproveSolution
from rest_framework.serializers import SerializerMethodField
from django.db.models import Q, F
from django.contrib.auth.models import User
from client.models import WXUser
from utils.defines import *


class ListQuestionSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(source='title')
    has_bad_solution = SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'sub_que_num', 'has_bad_solution']

    def get_has_bad_solution(self, que_obj: Question):
        return 1 if que_obj.has_bad_solution(self.context['admin']) else 0


class SubQuestionSerializer(serializers.ModelSerializer):
    options = SerializerMethodField()
    has_bad_solution = SerializerMethodField()

    class Meta:
        model = SubQuestion
        fields = ['id', 'number', 'stem', 'answer', 'options', 'has_bad_solution']

    def get_options(self, sub_question: SubQuestion):
        data = [sub_question.A, sub_question.B, sub_question.C, sub_question.D]
        return data

    def get_has_bad_solution(self, sub_que_obj: SubQuestion):
        return 1 if sub_que_obj.has_bad_solution(self.context['admin']) else 0


class DesignatedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'sub_que_num']


class SolutionSerializer(serializers.ModelSerializer):
    bad_solution = SerializerMethodField()
    approved = SerializerMethodField()
    author_username = SerializerMethodField()
    author_solution_sum = SerializerMethodField()
    author_likes = SerializerMethodField()
    author_reports = SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'content', 'likes', 'reports', 'bad_solution', 'approved', 'author_username',
                  'author_solution_sum', 'author_likes', 'author_reports']

    def get_bad_solution(self, solution_obj: Solution):
        if solution_obj.is_bad_solution():
            return 1
        else:
            return 0

    def get_approved(self, obj: Solution):
        return 1 if AdminApproveSolution.objects.filter(
            Q(admin=self.context['request'].user) & Q(solution=obj)).exists() else 0

    def get_author_username(self, solution_obj: Solution):
        return solution_obj.wxUser.user_name

    def get_author_solution_sum(self, solution_obj: Solution):
        return solution_obj.wxUser.solution_sum

    def get_author_likes(self, solution_obj: Solution):
        return solution_obj.wxUser.likes

    def get_author_reports(self, solution_obj: Solution):
        return solution_obj.wxUser.reports


class OperationRecordSerializer(serializers.ModelSerializer):
    name = SerializerMethodField()
    op_type = SerializerMethodField()

    class Meta:
        model = OperationRecord
        fields = ['name', 'op_type', 'description']

    def get_name(self, obj: OperationRecord):
        return obj.admin.username

    def get_op_type(self, obj: OperationRecord):
        return obj.operation


class GraphDataSerializer(serializers.ModelSerializer):
    value = SerializerMethodField()
    code = serializers.CharField(source='user_name')

    class Meta:
        model = WXUser
        fields = ['value', 'code']

    def get_value(self, wxuser_obj: WXUser):
        return wxuser_obj.__getattribute__(self.context['field_name'])
