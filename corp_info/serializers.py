from rest_framework import serializers
from .models import Corporation, SmartLogistics, Recruitment, News, UserProfile, Concern


class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = '__all__'


class CorporationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = ['corp_name']


class SmartLogisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SmartLogistics
        fields = '__all__'


class RecruitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class ConcernSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concern
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    concerns = ConcernSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'google_user_id', 'email', 'name', 'concerns']


