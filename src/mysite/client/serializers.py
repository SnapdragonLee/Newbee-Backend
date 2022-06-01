from .models import WrongQuestions, done_question, UserApproveSolution
from rest_framework import serializers
from models.basic.questions import Question, SubQuestion, Solution
from rest_framework.serializers import SerializerMethodField


class client_SubQuestionSerializer(serializers.ModelSerializer):
    options = SerializerMethodField()

    class Meta:
        model = SubQuestion
        fields = ['id', 'number', 'stem', 'options']

    def get_options(self, sub_question):
        data = [sub_question.A, sub_question.B, sub_question.C, sub_question.D]
        return data


class client_DetailSerializer(serializers.ModelSerializer):
    options = SerializerMethodField()
    option = SerializerMethodField()

    class Meta:
        model = SubQuestion
        fields = ['id', 'number', 'stem', 'options', 'answer', 'option']
        # fields = ['id', 'number', 'stem', 'options', 'answer']

    def get_options(self, sub_question):
        data = [sub_question.A, sub_question.B, sub_question.C, sub_question.D]
        return data

    def get_option(self, obj: SubQuestion):
        openid = self.context['openid']
        data = done_question.objects.get(wxUser_id=openid, subQuestion_id=obj.id)
        return data.option


class client_DesignatedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'sub_que_num']


class QuestionSer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'type']


class client_ListQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSer(read_only=True)

    class Meta:
        model = WrongQuestions
        fields = ['date', 'question']


class ClientSolutionSerializer(serializers.ModelSerializer):
    approved = SerializerMethodField()
    author_username = SerializerMethodField()
    author_solution_sum = SerializerMethodField()
    author_likes = SerializerMethodField()
    author_reports = SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['number', 'id', 'content', 'likes', 'reports', 'approved', 'author_username', 'author_solution_sum',
                  'author_likes', 'author_reports']

    def get_number(self, solution_obj: Solution):
        return self.context['sub_question_number']

    def get_approved(self, obj: Solution):
        openid = self.context['openid']

        query_set = UserApproveSolution.objects.filter(user__id=openid, solution=obj)
        if len(query_set) == 0:
            return 0
        else:
            return query_set[0].type

    def get_author_username(self, solution_obj: Solution):
        return solution_obj.wxUser.user_name

    def get_author_solution_sum(self, solution_obj: Solution):
        return solution_obj.wxUser.solution_sum

    def get_author_likes(self, solution_obj: Solution):
        return solution_obj.wxUser.likes

    def get_author_reports(self, solution_obj: Solution):
        return solution_obj.wxUser.reports


class SubQuestionSer(serializers.ModelSerializer):
    options = SerializerMethodField()

    class Meta:
        model = SubQuestion
        fields = ['number', 'stem', 'options', 'answer']

    def get_options(self, sub_question):
        data = [sub_question.A, sub_question.B, sub_question.C, sub_question.D]
        return data


class client_ListDoneQuestionSerializer(serializers.ModelSerializer):
    sub_question = SubQuestionSer(read_only=True)

    class Meta:
        model = done_question
        fields = ['sub_question', 'option']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubQuestion
        fields = ['number', 'answer']
