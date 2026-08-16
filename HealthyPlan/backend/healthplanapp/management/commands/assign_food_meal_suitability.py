from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from healthplanapp.models import Food
from healthplanapp.services.meal_plan.food_selector import MEAL_ROLE_ITEM_TYPE_MAP, MEAL_ROLE_KCAL_RANGE_MAP

EXCLUDED_NAME_TERMS = ["uncooked", "unprepared", "crude", "flour", "powder", "chitterlings", "variety meats", "by-products"]

class Command(BaseCommand):
    help = "Gán trạng thái phù hợp để tự động đưa Food vào Meal"

    @transaction.atomic
    def handle(self, *args, **options):
        Food.objects.update(is_meal_suitable=False)
        assigned_total = 0

        for meal_role, allowed_item_types in MEAL_ROLE_ITEM_TYPE_MAP.items():
            minimum_kcal, maximum_kcal = MEAL_ROLE_KCAL_RANGE_MAP[meal_role]
            updated = Food.objects.filter(active=True, meal_role=meal_role, item_type__in=allowed_item_types, processing_level__in=[Food.ProcessingLevel.UNPROCESSED, Food.ProcessingLevel.MINIMALLY_PROCESSED], kcal_per_100g__gte=minimum_kcal, kcal_per_100g__lte=maximum_kcal).update(is_meal_suitable=True)
            assigned_total += updated
            self.stdout.write(f"{meal_role}: {updated}")

        excluded_name_query = Q()

        for term in EXCLUDED_NAME_TERMS:
            excluded_name_query |= Q(name_en__icontains=term)

        excluded_total = Food.objects.filter(is_meal_suitable=True).filter(excluded_name_query).update(is_meal_suitable=False)

        self.stdout.write(f"Food đạt điều kiện ban đầu: {assigned_total}")
        self.stdout.write(f"Food bị loại theo tên: {excluded_total}")
        self.stdout.write(f"Food phù hợp Meal cuối cùng: {Food.objects.filter(is_meal_suitable=True).count()}")
        self.stdout.write(f"Food chỉ dùng để tra cứu: {Food.objects.filter(is_meal_suitable=False).count()}")