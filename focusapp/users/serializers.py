from rest_framework import serializers
from .models import CustomUser, Session

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'hwid', 'registration_date']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'session_key', 'created_at', 'expires_at']
