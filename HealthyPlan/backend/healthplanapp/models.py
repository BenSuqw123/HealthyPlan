from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Khách hàng"
        EXPERT = "expert", "Chuyên gia"
        ADMIN = "admin", "Quản trị viên"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HealthIssue(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class HealthProfile(BaseModel):
    class Gender(models.TextChoices):
        MALE = "male", "Nam"
        FEMALE = "female", "Nữ"

    class ActivityLevel(models.TextChoices):
        SEDENTARY = "sedentary", "Ít vận động"
        LIGHT = "light", "Vận động nhẹ"
        MODERATE = "moderate", "Vận động vừa"
        ACTIVE = "active", "Vận động nhiều"
        VERY_ACTIVE = "very_active", "Vận động rất nhiều"

    class Goal(models.TextChoices):
        LOSE_WEIGHT = "lose_weight", "Giảm cân"
        MAINTAIN_WEIGHT = "maintain_weight", "Duy trì cân nặng"
        GAIN_WEIGHT = "gain_weight", "Tăng cân"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="health_profile")
    gender = models.CharField(max_length=10, choices=Gender.choices)
    date_of_birth = models.DateField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    activity_level = models.CharField(max_length=20, choices=ActivityLevel.choices, default=ActivityLevel.MODERATE)
    goal = models.CharField(max_length=20, choices=Goal.choices, default=Goal.MAINTAIN_WEIGHT)
    target_weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    health_issues = models.ManyToManyField(HealthIssue, blank=True, related_name="health_profiles")

    def __str__(self):
        return self.user.username


class ExpertProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="expert_profile")
    specialization = models.CharField(max_length=150)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_experts")

    def __str__(self):
        return self.user.username


class HealthPlan(BaseModel):
    class PlanType(models.TextChoices):
        MEAL = "meal", "Kế hoạch ăn uống"
        EXERCISE = "exercise", "Kế hoạch luyện tập"

    class ReviewStatus(models.TextChoices):
        PENDING = "pending", "Chờ duyệt"
        APPROVED = "approved", "Đã duyệt"
        REJECTED = "rejected", "Từ chối"

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_plans")
    expert = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_health_plans")
    title = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=20, choices=PlanType.choices)
    content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    review_status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.PENDING)
    review_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title