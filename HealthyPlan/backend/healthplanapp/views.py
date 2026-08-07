from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User, HealthProfile, HealthIssue, ConsultationMessage
from .serializers import UserRegisterSerializer, UserResponseSerializer, UserUpdateSerializer, HealthProfileSerializer, HealthIssueSerializer, ConsultationMessageSerializer,ConsultationRequestSerializer
from .perms import HealthProfileOwner

from healthplanapp.services.consultation.consultation_service import prepare_consultation

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserResponseSerializer(user).data, status=status.HTTP_201_CREATED)
    
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

class HealthIssueViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = HealthIssue.objects.filter(active=True).select_related("parent").order_by("parent_id", "name")
    serializer_class = HealthIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConsultationViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = ConsultationMessage.objects.all()
    serializer_class = ConsultationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        queryset = ConsultationMessage.objects.all()
        serializer = ConsultationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = prepare_consultation(
            request.user,
            serializer.validated_data["message"],
            serializer.validated_data.get("session_id")
        )

        return Response(ConsultationMessageSerializer(message).data, status=status.HTTP_201_CREATED)