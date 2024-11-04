from rest_framework import serializers

from user.models import User
from scenic.models import Scenic
from reserve.models import Reserve
from strategy.models import Strategy
from evaluation.models import Evaluation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)
    checkPassword = serializers.CharField(required=True, max_length=100)
    nickname = serializers.CharField(required=True, max_length=100)


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)  
    avatarUrl = serializers.CharField(required=False, allow_blank=True)  
    address = serializers.CharField(required=False, allow_blank=True)  
    phone = serializers.CharField(required=False, allow_blank=True)  

    class Meta:
        model = User
        fields = '__all__'

class ScenicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenic
        fields = '__all__'
        depth = 1

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'
        depth = 1

class ReserveVOSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    scenic = serializers.SerializerMethodField()
    class Meta:
        model = Reserve
        fields = '__all__'

    def get_user(self, obj):
        users = User.objects.filter(id=obj.userId)
        return UserSerializer(users).data
    def get_scenic_list(self, obj):
        scenics = Scenic.objects.filter(id=obj.scenicId)
        return ScenicSerializer(scenics).data
    def get_evaluation(self, obj):
        comments = Evaluation.objects.filter(reserveId=obj.id)

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = '__all__'
        depth = 1

class StrategyVOSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Strategy
        fields = '__all__'
    def get_user(self, obj):
        users = User.objects.filter(id=obj.userId)
        return UserSerializer(users).data

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        depth = 1