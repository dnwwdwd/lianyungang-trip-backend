from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import User
from scenic.models import Scenic
from reserve.models import Reserve
from strategy.models import Strategy
from evaluation.models import Evaluation
from scenic_star.models import ScenicStar
from strategy_star.models import StrategyStar


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
        try:
            user = User.objects.get(id=obj.userId)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None

    def get_scenic(self, obj):
        try:
            scenic = Scenic.objects.get(id=obj.userId)
            return ScenicSerializer(scenic).data
        except Scenic.DoesNotExist:
            return None

    def get_evaluation(self, obj):
        try:
            evaluation = Evaluation.objects.get(reserveId=obj.id)
            return EvaluationSerializer(evaluation).data
        except Evaluation.DoesNotExist:
            return None


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
        try:
            user = User.objects.get(id=obj.userId)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        depth = 1


class ScenicStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenicStar
        fields = '__all__'


class StrategyStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyStar
        fields = '__all__'


class ScenicStarVOSerializer(serializers.ModelSerializer):
    scenic = serializers.SerializerMethodField()

    class Meta:
        model = ScenicStar
        fields = '__all__'

    def get_scenic(self, obj):
        try:
            scenic = Scenic.objects.get(id=obj.scenicId)
            return ScenicSerializer(scenic).data
        except Scenic.DoesNotExist:
            return None


class StrategyStarVOSerializer(serializers.ModelSerializer):
    strategy = serializers.SerializerMethodField()
    class Meta:
        model = StrategyStar
        fields = '__all__'
    def get_strategy(self, obj):
        try:
            strategy = Strategy.objects.get(id=obj.strategyId)
            return StrategyVOSerializer(strategy).data
        except Strategy.DoesNotExist:
            return None