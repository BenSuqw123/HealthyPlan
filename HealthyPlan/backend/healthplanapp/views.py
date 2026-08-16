from datetime import date
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User, HealthProfile, HealthIssue, ConsultationMessage, ConsultationSession, Food, HealthPlan
from .serializers import UserRegisterSerializer, UserResponseSerializer, UserUpdateSerializer, HealthProfileSerializer, HealthIssueSerializer, ConsultationMessageSerializer, ConsultationRequestSerializer, ConsultationSessionSerializer, ConsultationSessionUpdateSerializer, FoodSerializer, MealHealthPlanSerializer, MealPlanGenerateSerializer, MealPlanGenerationResultSerializer
from .perms import HealthProfileOwner
from .paginators import FoodPaginator
from .services.consultation.consultation_service import prepare_consultation
from .services.meal_plan.builder import OneDayMealPlanBuilder

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserResponseSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(methods=["get", "patch"], detail=False, url_path="current-user", permission_classes=[permissions.IsAuthenticated])
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
        serializer = ConsultationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = prepare_consultation(request.user, serializer.validated_data["message"], serializer.validated_data.get("session_id"))

        return Response(ConsultationMessageSerializer(message).data, status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=False, url_path="sessions")
    def sessions(self, request):
        sessions = request.user.consultation_sessions.all().order_by("-updated_at")

        return Response(ConsultationSessionSerializer(sessions, many=True).data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False, url_path=r"sessions/(?P<session_id>[^/.]+)/messages")
    def session_messages(self, request, session_id=None):
        session = get_object_or_404(ConsultationSession, id=session_id, user=request.user)
        messages = session.messages.all().order_by("created_at")

        return Response(ConsultationMessageSerializer(messages, many=True).data, status=status.HTTP_200_OK)

    @action(methods=["patch", "delete"], detail=False, url_path=r"sessions/(?P<session_id>[^/.]+)")
    def session_detail(self, request, session_id=None):
        session = get_object_or_404(ConsultationSession, id=session_id, user=request.user)

        if request.method == "PATCH":
            serializer = ConsultationSessionUpdateSerializer(session, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            session = serializer.save()

            return Response(ConsultationSessionSerializer(session).data, status=status.HTTP_200_OK)

        session.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Food.objects.filter(active=True).order_by("name_vi")
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FoodPaginator
    search_fields = ["food_id", "name_vi", "name_en"]
    filterset_fields = ["category_vi", "item_type", "processing_level"]
    ordering_fields = ["name_vi", "kcal_per_100g", "protein_g", "fat_g", "carb_g", "fiber_g", "sodium_mg", "potassium_mg", "saturated_fat_g"]
    ordering = ["name_vi"]

class HealthPlanViewSet(viewsets.ViewSet):
    queryset = HealthPlan.objects.filter(active=True, plan_type=HealthPlan.PlanType.MEAL)
    serializer_class = MealHealthPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user).prefetch_related("meals__items__food").order_by("-created_date")

    def list(self, request):
        plans = self.get_queryset()

        return Response(MealHealthPlanSerializer(plans, many=True).data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        plan = get_object_or_404(self.get_queryset(), id=pk)

        return Response(MealHealthPlanSerializer(plan).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        plan = get_object_or_404(self.get_queryset(), id=pk)
        plan.active = False
        plan.save(update_fields=["active", "updated_date"])

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False, url_path="generate-meal-plan")
    def generate_meal_plan(self, request):
        serializer = MealPlanGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = HealthProfile.objects.filter(user=request.user, active=True).first()

        if profile is None:
            return Response({"detail": "Bạn chưa có hồ sơ sức khỏe."}, status=status.HTTP_404_NOT_FOUND)

        plan_date = serializer.validated_data.get("plan_date") or date.today()
        title = serializer.validated_data.get("title", "Kế hoạch ăn uống một ngày")

        if HealthPlan.objects.filter(customer=request.user, active=True, plan_type=HealthPlan.PlanType.MEAL, start_date__lte=plan_date, end_date__gte=plan_date).exists():
            return Response({"plan_date": "Ngày này đã có kế hoạch ăn uống."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = OneDayMealPlanBuilder(profile, plan_date, title).build()
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        adjustment_result = result["adjustment_result"]
        result_data = {"health_plan": result["health_plan"], "status": adjustment_result["status"], "attempt_count": adjustment_result["attempt_count"], "adjustments": adjustment_result["adjustments"], "evaluation": result["evaluation"]}

        return Response(MealPlanGenerationResultSerializer(result_data).data, status=status.HTTP_201_CREATED)