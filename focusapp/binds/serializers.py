from rest_framework import serializers
from .models import Bind


class BindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bind
        fields = ['id', 'user', 'bind_name', 'script_path', 'key_binding']
