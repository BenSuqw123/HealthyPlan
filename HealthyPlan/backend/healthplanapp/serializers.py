from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers
from django.utils import timezone as django_timezone

from .models import User, HealthProfile, HealthIssue, ConsultationSession, ConsultationMessage, Food, HealthPlan, Meal, MealItem


class UserResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "is_active", "date_joined")
        read_only_fields = fields


class UserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "password_confirm")

    def validate_email(self, value):
        normalized_email = value.strip().lower()

        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("Email này đã được sử dụng.")

        return normalized_email

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Mật khẩu xác nhận không khớp."})

        candidate_user = User(username=attrs.get("username"), email=attrs.get("email"), first_name=attrs.get("first_name", ""), last_name=attrs.get("last_name", ""))

        try:
            validate_password(password, user=candidate_user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)}) from exc

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def validate_email(self, value):
        normalized_email = value.strip().lower()
        queryset = User.objects.filter(email__iexact=normalized_email)

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Email này đã được sử dụng.")

        return normalized_email


class HealthIssueSerializer(serializers.ModelSerializer):

    parent_name = serializers.CharField(source="parent.name", read_only=True, default=None)

    class Meta:
        model = HealthIssue
        fields = ("id", "code", "name", "description", "parent", "parent_name", "kind", "selectable")
        read_only_fields = ("id", "parent_name")

    def validate_code(self, value):
        normalized_code = value.strip().lower()
        queryset = HealthIssue.objects.filter(code__iexact=normalized_code)

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Mã bệnh lý này đã tồn tại.")

        return normalized_code

    def validate_name(self, value):
        normalized_name = value.strip()

        if not normalized_name:
            raise serializers.ValidationError("Tên bệnh lý không được để trống.")

        return normalized_name


class HealthProfileSerializer(serializers.ModelSerializer):
    health_issues = HealthIssueSerializer(many=True, read_only=True)
    class Meta:
        model = HealthProfile
        fields = ("id", "date_of_birth", "gender", "weight", "height", "activity_level", "goal", "target_weight","health_issues", "other_health_issue")
        read_only_fields = ("id",)

    def validate_date_of_birth(self, value):
        if value > django_timezone.localdate():
            raise serializers.ValidationError("Ngày sinh không được trong tương lai!")

        return value

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Cân nặng phải lớn hơn 0!")

        return value

    def validate_height(self, value):
        if value <= 0:
            raise serializers.ValidationError("Chiều cao phải lớn hơn 0!")

        return value

    def validate_target_weight(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Cân nặng mục tiêu phải lớn hơn 0!")

        return value

    def validate(self, attrs):
        current_weight = attrs.get("weight", getattr(self.instance, "weight", None))
        goal = attrs.get("goal", getattr(self.instance, "goal", None))
        target_weight = attrs.get("target_weight", getattr(self.instance, "target_weight", None))

        if goal == "maintain_weight":
            attrs["target_weight"] = current_weight
            return attrs

        if goal in ("lose_weight", "gain_weight") and target_weight is None:
            raise serializers.ValidationError({"target_weight": "Vui lòng nhập cân nặng mục tiêu."})

        if goal == "lose_weight" and current_weight is not None and target_weight >= current_weight:
            raise serializers.ValidationError({"target_weight": "Mục tiêu giảm cân phải nhỏ hơn cân nặng hiện tại."})

        if goal == "gain_weight" and current_weight is not None and target_weight <= current_weight:
            raise serializers.ValidationError({"target_weight": "Mục tiêu tăng cân phải lớn hơn cân nặng hiện tại."})

        return attrs

class ConsultationRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    session_id = serializers.UUIDField(required=False, allow_null=True)

    def validate_message(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Nội dung câu hỏi không được để trống.")

        return value

class ConsultationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationMessage
        fields = ("id", "session", "role", "content", "created_at")

class ConsultationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationSession
        fields = ("id", "title", "created_at", "updated_at")
        
class ConsultationSessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationSession
        fields = ("title",)

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Tiêu đề không được để trống.")

        return value

class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ("id", "food_id", "source_name", "name_vi", "name_en", "category_vi", "category_en", "item_type", "processing_level", "kcal_per_100g", "protein_g", "fat_g", "carb_g", "fiber_g", "sodium_mg", "potassium_mg", "saturated_fat_g")
        read_only_fields = fields

class MealItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)

    class Meta:
        model = MealItem
        fields = ["id", "food", "serving_grams"]

class MealSerializer(serializers.ModelSerializer):
    items = MealItemSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ["id", "date", "meal_type", "items"]

class MealHealthPlanSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)

    class Meta:
        model = HealthPlan
        fields = ["id", "title", "plan_type", "start_date", "end_date", "review_status", "review_note", "meals"]

class MealPlanGenerateSerializer(serializers.Serializer):
    plan_date = serializers.DateField(required=False)
    title = serializers.CharField(max_length=255, required=False, allow_blank=False)

class MealPlanGenerationResultSerializer(serializers.Serializer):
    health_plan = MealHealthPlanSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    attempt_count = serializers.IntegerField(read_only=True)
    adjustments = serializers.JSONField(read_only=True)
    evaluation = serializers.JSONField(read_only=True)