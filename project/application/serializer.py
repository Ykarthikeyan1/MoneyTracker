from rest_framework import serializers
from .models import friend

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model=friend
        fields='__all__'