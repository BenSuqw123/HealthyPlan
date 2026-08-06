from time import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers

from .models import User, HealthProfile


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

class HealthProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthProfile
        fields = ("id", "date_of_birth", "gender", "weight", "height", "activity_level", "goal", "target_weight")
        read_only_fields = ("id")

    def validate_date_of_birth(self, value):
        if value > timezone.localdate():
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
    