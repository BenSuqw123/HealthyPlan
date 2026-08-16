from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from healthplanapp.models import Food

CARBOHYDRATE_CATEGORIES = ["Ngũ cốc và mì/nui", "Ngũ cốc và sản phẩm chế biến", "Khoai củ và sản phẩm chế biến"]
PROTEIN_CATEGORIES = ["Thịt bò và sản phẩm từ thịt bò", "Thịt gia cầm", "Thịt heo và sản phẩm từ thịt heo", "Cá, hải sản và sản phẩm liên quan", "Thủy sản và sản phẩm chế biến", "Đậu và sản phẩm từ đậu", "Trứng và sản phẩm chế biến"]
VEGETABLE_CATEGORIES = ["Rau củ và sản phẩm từ rau củ", "Rau, quả, củ dùng làm rau"]
BREAKFAST_SIDE_CATEGORIES = ["Trái cây và nước ép", "Quả chín", "Sữa, trứng và sản phẩm liên quan", "Sữa và sản phẩm chế biến"]

ROLE_CATEGORY_MAP = {Food.MealRole.CARBOHYDRATE: CARBOHYDRATE_CATEGORIES, Food.MealRole.PROTEIN: PROTEIN_CATEGORIES, Food.MealRole.VEGETABLE: VEGETABLE_CATEGORIES, Food.MealRole.BREAKFAST_SIDE: BREAKFAST_SIDE_CATEGORIES}

class Command(BaseCommand):
    help = "Gán vai trò bữa ăn cho dữ liệu Food hiện có"

    def handle(self, *args, **options):
        updated_total = 0

        with transaction.atomic():
            for meal_role, categories in ROLE_CATEGORY_MAP.items():
                updated = Food.objects.filter(category_vi__in=categories).update(meal_role=meal_role)
                updated_total += updated
                self.stdout.write(f"{meal_role}: {updated}")

        unassigned_categories = Food.objects.filter(meal_role=Food.MealRole.OTHER).values("category_vi").annotate(total=Count("id")).order_by("-total")

        self.stdout.write(f"Đã gán role: {updated_total}")
        self.stdout.write(f"Food còn ở role other: {Food.objects.filter(meal_role=Food.MealRole.OTHER).count()}")

        for category in unassigned_categories:
            self.stdout.write(f"- {category['category_vi']}: {category['total']}")