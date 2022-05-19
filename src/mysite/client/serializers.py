from .models import WXUser, WrongQuestions, done_question
from rest_framework import serializers
from administrator.models import Question, SubQuestion, Solution
from rest_framework.serializers import SerializerMethodField
from client.models import UserApproveSolution


class ListUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user_name')
    numm = serializers.IntegerField(source='total_choice')
    numc = serializers.IntegerField(source='total_cloze')
    numr = serializers.IntegerField(source='total_reading')
    right_choice_que = serializers.IntegerField(source='right_choice')
    right_reading_que = serializers.IntegerField(source='right_reading')
    right_cloze_que = serializers.IntegerField(source='right_cloze')

    class Meta:
        model = WXUser
        fields = ['id', 'name', "numm", 'numc', 'numr', 'right_choice_que', 'right_reading_que', 'right_cloze_que']

    # 这里之所以这么写，是因为前端需要的json中的key值，为name、numm、numc、numr故也需要在序列化时，把key的名字改成这些
    # 如果前端要求json中key的值与模型中的字段名相同，则可以按以下写法
    '''
    class ListUserSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = WXUser
            fields = ['user_name', "total_choice", 'total_cloze', 'total_reading'] 
            #这个fields列表中的字符串就是字段名
            #这样序列化器生成的字典中的key值与字段名相同
    '''


class client_SubQuestionSerializer(serializers.ModelSerializer):
    options = SerializerMethodField()

    class Meta:
        model = SubQuestion
        fields = ['id', 'number', 'stem', 'options']

    def get_options(self, sub_question):
        data = [sub_question.A, sub_question.B, sub_question.C, sub_question.D]
        return data


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
        fields = ['id', 'content', 'likes', 'reports', 'approved', 'author_username', 'author_solution_sum',
                  'author_likes', 'author_reports']

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
        return Solution.objects.filter(wxUser=solution_obj.wxUser).count()

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
