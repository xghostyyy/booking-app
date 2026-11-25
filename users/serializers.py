from rest_framework import serializers
from users.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "executor", "duration_minutes", "price", "format",]
