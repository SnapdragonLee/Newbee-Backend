from rest_framework import serializers
from .models import Question, SubQuestion
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
        fields = ['id', 'stem', 'answer', 'options']

    def get_options(self, sub_question):
        data = [sub_question.A, sub_question.B, sub_question.C, sub_question.D]
        return data


class DesignatedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'sub_que_num']
