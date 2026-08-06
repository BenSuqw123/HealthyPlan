from backend.healthplanapp.serializers import HealthProfileSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, HealthProfile
from .serializers import UserRegisterSerializer, UserResponseSerializer, UserUpdateSerializer
from .perms import HealthProfileOwner

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserResponseSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(methods=['get','patch'],detail=False, url_path="current-user", permission_classes=[permissions.IsAuthenticated])
    def current_user(self, request):
        user = request.user

        if request.method == "PATCH":
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

        return Response(UserResponseSerializer(user).data, status=status.HTTP_200_OK)
    
class HealthProfileViewSet(viewsets.ViewSet, generics.CreateAPIView):

    queryset = HealthProfile.objects.all()
    serializer_class = HealthProfileSerializer
    permission_classes = [permissions.IsAuthenticated, HealthProfileOwner]

    def create(self, request, *args, **kwargs):
        if HealthProfile.objects.filter(user=request.user).exists():
            return Response({"detail": "Bạn đã có hồ sơ sức khỏe."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HealthProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save(user=request.user)

        return Response(HealthProfileSerializer(profile).data, status=status.HTTP_201_CREATED)

    @action(methods=["get", "patch"], detail=False, url_path="current-profile")
    def current_profile(self, request):
        profile = HealthProfile.objects.filter(user=request.user).first()

        if profile is None:
            return Response({"detail": "Bạn chưa có hồ sơ sức khỏe."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, profile)

        if request.method == "PATCH":
            serializer = HealthProfileSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            profile = serializer.save()

        return Response(HealthProfileSerializer(profile).data, status=status.HTTP_200_OK)