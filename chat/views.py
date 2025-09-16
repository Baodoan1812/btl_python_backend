# chat/views.py
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

# Chỉ user đăng nhập mới truy cập được
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Lọc conversation chỉ của user hiện tại
        user = self.request.user
        return Conversation.objects.filter(my_id=user) | Conversation.objects.filter(other_id=user)
    @action(detail=False, methods=["post"], url_path="get-or-create")
    def get_or_create_conversation(self, request):
        """
        API: POST /chat/conversations/get-or-create/
        Body: {"other_user_id": 2}
        """
        user = request.user
        other_user_id = request.data.get("other_user_id")

        if not other_user_id:
            return Response({"error": "other_user_id is required"}, status=400)

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({"error": "Other user not found"}, status=404)

        # Tìm conv đã tồn tại
        conversation = Conversation.objects.filter(
            (Q(my_id=user) & Q(other_id=other_user)) |
            (Q(my_id=other_user) & Q(other_id=user))
        ).first()

        # Nếu chưa có thì tạo
        if not conversation:
            conversation = Conversation.objects.create(my_id=user, other_id=other_user)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)


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
