from rest_framework import generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .serializers import UserCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # bảo vệ endpoint, chỉ user đã login mới vào được

    def get(self, request):
        user = request.user  # đây là user được xác thực từ token
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
        })
