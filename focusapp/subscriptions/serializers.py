
from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class HwidCheckSerializer(serializers.Serializer):
    hwid = serializers.CharField(max_length=255)


class SubscriptionUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    subscription_type = serializers.CharField(max_length=50)
    duration_days = serializers.IntegerField()  # Новое поле для количества дней
