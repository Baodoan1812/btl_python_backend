# chat/serializers.py
from rest_framework import serializers
from .models import Conversation, Message
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class ConversationSerializer(serializers.ModelSerializer):
    my_id = serializers.PrimaryKeyRelatedField(read_only=True)
    other_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Conversation
        fields = ['id', 'my_id', 'other_id', 'created_at', 'updated_at']
    def create(self, validated_data):
        validated_data['my_id'] = self.context['request'].user
        return super().create(validated_data)

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'created_at', 'updated_at']
