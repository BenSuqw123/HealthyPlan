import uuid
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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

    class Kind(models.TextChoices):
        DISEASE = "disease", "Nhóm bệnh"
        TYPE = "type", "Loại bệnh"
        STAGE = "stage", "Giai đoạn"

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.DISEASE)
    selectable = models.BooleanField(default=True)

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
    other_health_issue = models.TextField(null=True, blank=True)
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

class ConsultationSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consultation_sessions")
    title = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.id}"


class ConsultationMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    session = models.ForeignKey(ConsultationSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    intent = models.CharField(max_length=50, blank=True, default="")
    citations = models.JSONField(default=list, blank=True)
    profile_snapshot = models.JSONField(default=dict, blank=True)
    safety_metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.session_id}"

class Food(BaseModel):
    class ItemType(models.TextChoices):
        RAW_INGREDIENT = "raw_ingredient", "Nguyên liệu thô"
        COOKED_FOOD = "cooked_food", "Thực phẩm đã nấu"
        BASIC_FOOD = "basic_food", "Thực phẩm cơ bản"
        BEVERAGE = "beverage", "Đồ uống"
        PREPARED_FOOD = "prepared_food", "Thực phẩm chế biến sẵn"

    class ProcessingLevel(models.TextChoices):
        UNPROCESSED = "unprocessed", "Chưa chế biến"
        MINIMALLY_PROCESSED = "minimally_processed", "Chế biến tối thiểu"
        PROCESSED = "processed", "Đã chế biến"
    class MealRole(models.TextChoices):
        CARBOHYDRATE = "carbohydrate", "Tinh bột"
        PROTEIN = "protein", "Chất đạm"
        VEGETABLE = "vegetable", "Rau củ"
        BREAKFAST_SIDE = "breakfast_side", "Thực phẩm phụ buổi sáng"
        OTHER = "other", "Khác"
        
    food_id = models.CharField(max_length=20, unique=True)
    source_name = models.CharField(max_length=50)
    name_vi = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True, default="")
    category_vi = models.CharField(max_length=100)
    category_en = models.CharField(max_length=100)
    item_type = models.CharField(max_length=30, choices=ItemType.choices)
    processing_level = models.CharField(max_length=30, choices=ProcessingLevel.choices)
    meal_role = models.CharField(max_length=30, choices=MealRole.choices, default=MealRole.OTHER)
    is_meal_suitable = models.BooleanField(default=False)

    kcal_per_100g = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    protein_g = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    fat_g = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    carb_g = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    fiber_g = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(0)])
    sodium_mg = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(0)])
    potassium_mg = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(0)])
    saturated_fat_g = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.name_vi

class Meal(BaseModel):
    class MealType(models.TextChoices):
        BREAKFAST = "breakfast", "Bữa sáng"
        LUNCH = "lunch", "Bữa trưa"
        DINNER = "dinner", "Bữa tối"

    health_plan = models.ForeignKey(HealthPlan, on_delete=models.CASCADE, related_name="meals")
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MealType.choices)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["health_plan", "date", "meal_type"], name="unique_meal_per_plan_date_type")]

    def __str__(self):
        return f"{self.health_plan.title} - {self.date} - {self.get_meal_type_display()}"

class MealItem(BaseModel):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(Food, on_delete=models.PROTECT, related_name="meal_items")
    serving_grams = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["meal", "food"], name="unique_food_per_meal")]

    def __str__(self):
        return f"{self.food.name_vi} - {self.serving_grams}g"

class HealthConditionNutrientRule(BaseModel):
    class RuleType(models.TextChoices):
        AVOID = "avoid", "Tránh"
        INDIVIDUALIZE = "individualize", "Cá nhân hóa"
        LIMIT = "limit", "Hạn chế"
        MODERATE = "moderate", "Điều chỉnh"
        MONITOR = "monitor", "Theo dõi"
        PRIORITIZE = "prioritize", "Ưu tiên"

    class Priority(models.TextChoices):
        HIGH = "high", "Cao"
        MEDIUM = "medium", "Trung bình"
        LOW = "low", "Thấp"

    rule_id = models.CharField(max_length=100, unique=True)
    condition_code = models.CharField(max_length=100, db_index=True)
    evaluation_field = models.CharField(max_length=50)
    rule_type = models.CharField(max_length=20, choices=RuleType.choices)
    priority = models.CharField(max_length=10, choices=Priority.choices)
    threshold_value = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(0)])
    threshold_unit = models.CharField(max_length=50, blank=True, default="")
    applies_when = models.CharField(max_length=100, blank=True, default="")
    recommendation_vi = models.TextField()
    clinical_caution_vi = models.TextField(blank=True, default="")
    source_name = models.CharField(max_length=255)
    source_url = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.condition_code} - {self.evaluation_field}"

class Exercise(BaseModel):
    class METtyepe(models.TextChoices):
        ADULT = "MET", "Adult"
        OLDER_ADULT = "MET_60_PLUS", "Người từ 60 tuổi"
    class Intensity(models.TextChoices):
        SEDENTARY = "sedentary", "Ít vận động"
        LIGHT = "light", "Nhẹ"
        MODERATE = "moderate", "Vừa"
        VIGOROUS = "vigorous", "Cao"
    activity_id = models.CharField(max_length=50, unique=True)
    category_name = models.CharField(max_length=150)
    description = models.TextField()
    met_value = models.DecimalField(max_digits=5, decimal_places=2)
    met_type = models.CharField(max_length=20, choices=MetType.choices)
    intensity_level = models.CharField(max_length=20, choices=Intensity.choices)
    