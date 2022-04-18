from rest_framework import serializers
from .models import WXUser


class ListUserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='user_name')
    numm = serializers.CharField(source='total_choice')
    numc = serializers.CharField(source='total_cloze')
    numr = serializers.CharField(source='total_reading')

    class Meta:
        model = WXUser
        fields = ['name', "numm", 'numc', 'numr','id']

    #这里之所以这么写，是因为前端需要的json中的key值，为name、numm、numc、numr故也需要在序列化时，把key的名字改成这些
    #如果前端要求json中key的值与模型中的字段名相同，则可以按以下写法
    '''
    class ListUserSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = WXUser
            fields = ['user_name', "total_choice", 'total_cloze', 'total_reading'] 
            #这个fields列表中的字符串就是字段名
            #这样序列化器生成的字典中的key值与字段名相同
    '''
