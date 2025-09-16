# chat/views.py
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

# Chỉ user đăng nhập mới truy cập được
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Lọc conversation chỉ của user hiện tại
        user = self.request.user
        return Conversation.objects.filter(my_id=user) | Conversation.objects.filter(other_id=user)



class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Lấy message theo conversation_id từ query param:
        GET /chat/messages/?conversation_id=1
        """
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            # Kiểm tra user có tham gia conversation không
            if self.request.user not in [conversation.my_id, conversation.other_id]:
                return Message.objects.none()
            return Message.objects.filter(conversation=conversation)
        return Message.objects.none()  # mặc định trả về rỗng nếu không truyền conversation_id

    def perform_create(self, serializer):
        """
        Khi tạo message, set sender là user hiện tại.
        """
        serializer.save(sender=self.request.user)
