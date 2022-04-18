from rest_framework import serializers
from .models import Question


class ListQuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='title')

    class Meta:
        model = Question
        fields = ['text', 'sub_que_num', 'id']



class DesignatedQuestionSerializer(serializers.ModelSerializer):



    class Meta:
        model = Question
        fields = ['title','text', 'sub_que_num', 'id']


