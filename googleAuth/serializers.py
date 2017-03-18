from rest_framework import serializers

class GoogleTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
