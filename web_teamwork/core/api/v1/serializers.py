from rest_framework import serializers


class UserLeaderboardSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    total_prize = serializers.IntegerField()
