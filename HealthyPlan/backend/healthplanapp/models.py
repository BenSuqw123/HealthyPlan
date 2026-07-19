from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Quản trị viên"
        USER = "user", "Người dùng"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER, db_index=True)

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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="health_profile")
    gender = models.CharField(max_length=10, choices=Gender.choices)
    date_of_birth = models.DateField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    activity_level = models.CharField(max_length=20, choices=ActivityLevel.choices, default=ActivityLevel.MODERATE)
    goal = models.CharField(max_length=20, choices=Goal.choices, default=Goal.MAINTAIN_WEIGHT)
    target_weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.user.username


class HealthIssue(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserHealthIssue(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="health_issues")
    health_issue = models.ForeignKey(HealthIssue, on_delete=models.PROTECT, related_name="affected_users")
    diagnosed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.health_issue.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "health_issue"], name="unique_user_health_issue")
        ]


class Nutrient(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    name_vi = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150, blank=True)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name_vi} ({self.unit})"


class Food(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    name_vi = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name_vi


class FoodNutrient(BaseModel):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="nutrients")
    nutrient = models.ForeignKey(Nutrient, on_delete=models.PROTECT, related_name="foods")
    amount_per_100g = models.DecimalField(max_digits=12, decimal_places=4)

    def __str__(self):
        return f"{self.food} - {self.nutrient}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["food", "nutrient"], name="unique_food_nutrient")
        ]


class NutrientHealthRiskRule(BaseModel):
    class RuleType(models.TextChoices):
        MINIMUM = "minimum", "Tối thiểu"
        MAXIMUM = "maximum", "Tối đa"
        LIMIT = "limit", "Hạn chế"
        AVOID = "avoid", "Nên tránh"
        ENCOURAGE = "encourage", "Khuyến khích"

    health_issue = models.ForeignKey(HealthIssue, on_delete=models.CASCADE, related_name="nutrient_rules")
    nutrient = models.ForeignKey(Nutrient, on_delete=models.PROTECT, related_name="health_rules")
    rule_type = models.CharField(max_length=20, choices=RuleType.choices)
    minimum_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    maximum_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    unit = models.CharField(max_length=30, blank=True)
    recommendation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.health_issue} - {self.nutrient}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["health_issue", "nutrient", "rule_type"],
                name="unique_nutrient_health_rule"
            )
        ]


class ExerciseActivity(BaseModel):
    class UserGroup(models.TextChoices):
        ADULT = "adult", "Người trưởng thành"
        OLDER_ADULT = "older_adult", "Người cao tuổi"
        WHEELCHAIR = "wheelchair", "Người dùng xe lăn"

    code = models.CharField(max_length=100, unique=True)
    name_vi = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=150, blank=True)
    user_group = models.CharField(max_length=20, choices=UserGroup.choices)
    met_value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name_vi

