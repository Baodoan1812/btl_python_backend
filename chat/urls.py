# chat/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from .views import StartChatbotConversation
from .views import ChatbotReplyView
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
urlpatterns = [
    path('', include(router.urls)),
    path('start-chatbot/', StartChatbotConversation.as_view(), name='start-chatbot'),
    path('chatbot-reply/', ChatbotReplyView.as_view(), name='chatbot-reply'),
]
