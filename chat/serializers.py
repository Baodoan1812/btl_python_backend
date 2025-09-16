# chat/serializers.py
from django.db.models import Q
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
        user = self.context['request'].user
        other_user = validated_data['other_id']

        # Kiểm tra nếu conv đã tồn tại (theo cả 2 chiều)
        conversation = Conversation.objects.filter(
        (Q(my_id=user) & Q(other_id=other_user)) |
        (Q(my_id=other_user) & Q(other_id=user))
        ).first()

        if conversation:
            return conversation

        # nếu chưa có thì tạo mới
        conversation = Conversation.objects.create(my_id=user, other_id=other_user)
        return conversation


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'created_at', 'updated_at']
