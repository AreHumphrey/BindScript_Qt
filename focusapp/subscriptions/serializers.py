from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class HwidCheckSerializer(serializers.Serializer):
    hwid = serializers.CharField(max_length=255)
