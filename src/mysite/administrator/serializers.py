from rest_framework import serializers
from .models import Question, SubQuestion, Solution
from rest_framework.serializers import SerializerMethodField


class ListQuestionSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(source='title')

    class Meta:
        model = Question
        fields = ['title', 'sub_que_num', 'id']


class SubQuestionSerializer(serializers.ModelSerializer):
    options = SerializerMethodField()

    class Meta:
        model = SubQuestion
        fields = ['id', 'number', 'stem', 'answer', 'options']

    def get_options(self, sub_question):
        data = [sub_question.A, sub_question.B, sub_question.C, sub_question.D]
        return data


class DesignatedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'sub_que_num']


class SolutionSerializer(serializers.ModelSerializer):
    bad_solution = SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'content', 'likes', 'reports', 'bad_solution']

    def get_bad_solution(self, solution_obj: Solution):
        if solution_obj.bad_solution:
            return 1
        else:
            return 0
