from rest_framework import serializers
from .models import WXUser


class ListUserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='user_name')
    numm = serializers.CharField(source='total_choice')
    numc = serializers.CharField(source='total_cloze')
    numr = serializers.CharField(source='total_reading')

    class Meta:
        model = WXUser
        fields = ['name', "numm", 'numc', 'numr']
