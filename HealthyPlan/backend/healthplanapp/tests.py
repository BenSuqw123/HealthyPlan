from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, HealthProfile, HealthPlan, Meal, MealItem, Food
from .services.meal_plan.allocation import allocate_meal_calories
from .services.meal_plan.plan_evaluator import evaluate_calorie_target

class MealPlanCalculationTests(TestCase):
    def test_allocate_meal_calories(self):
        result = allocate_meal_calories(Decimal("2117.56"))

        self.assertEqual(result["breakfast"], Decimal("529.39"))
        self.assertEqual(result["lunch"], Decimal("847.02"))
        self.assertEqual(result["dinner"], Decimal("741.15"))
        self.assertEqual(sum(result.values()), Decimal("2117.56"))

    def test_evaluate_calorie_target(self):
        target_calories = Decimal("2117.56")
        below_result = evaluate_calorie_target(Decimal("1800"), target_calories)
        passed_result = evaluate_calorie_target(Decimal("2117.56"), target_calories)
        above_result = evaluate_calorie_target(Decimal("2500"), target_calories)

        self.assertEqual(below_result["status"], "below_target")
        self.assertEqual(passed_result["status"], "passed")
        self.assertEqual(above_result["status"], "above_target")

    def test_calorie_tolerance_boundaries_are_passed(self):
        target_calories = Decimal("2117.56")
        minimum_result = evaluate_calorie_target(Decimal("1905.80"), target_calories)
        maximum_result = evaluate_calorie_target(Decimal("2329.32"), target_calories)

        self.assertEqual(minimum_result["status"], "passed")
        self.assertEqual(maximum_result["status"], "passed")

class HealthPlanAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="customer", email="customer@example.com", password="123456")
        self.other_user = User.objects.create_user(username="other_customer", email="other_customer@example.com", password="123456")
        self.health_profile = HealthProfile.objects.create(user=self.user, gender=HealthProfile.Gender.MALE, date_of_birth=date(2004, 5, 10), weight=Decimal("70.00"), height=Decimal("175.00"), activity_level=HealthProfile.ActivityLevel.MODERATE, goal=HealthProfile.Goal.LOSE_WEIGHT)
        self.plan_date = date(2026, 8, 20)
        self.plan = HealthPlan.objects.create(customer=self.user, title="Kế hoạch test", plan_type=HealthPlan.PlanType.MEAL, content="", start_date=self.plan_date, end_date=self.plan_date)
        self.foods = [self.create_food(1, Food.MealRole.CARBOHYDRATE), self.create_food(2, Food.MealRole.PROTEIN), self.create_food(3, Food.MealRole.VEGETABLE)]

        for meal_type in ["breakfast", "lunch", "dinner"]:
            meal = Meal.objects.create(health_plan=self.plan, date=self.plan_date, meal_type=meal_type)
            MealItem.objects.bulk_create([MealItem(meal=meal, food=food, serving_grams=Decimal("100.00")) for food in self.foods])

    def create_food(self, number, meal_role):
        return Food.objects.create(food_id=f"TEST{number:06d}", source_name="TEST", name_vi=f"Thực phẩm test {number}", name_en=f"Test food {number}", category_vi="Danh mục test", category_en="Test category", item_type=Food.ItemType.COOKED_FOOD, processing_level=Food.ProcessingLevel.MINIMALLY_PROCESSED, meal_role=meal_role, is_meal_suitable=True, kcal_per_100g=Decimal("100.000"), protein_g=Decimal("10.000"), fat_g=Decimal("5.000"), carb_g=Decimal("15.000"), fiber_g=Decimal("2.000"), sodium_mg=Decimal("10.000"), potassium_mg=Decimal("100.000"), saturated_fat_g=Decimal("1.000"))

    def test_owner_can_list_health_plans(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("healthplan-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.plan.id)
        self.assertEqual(len(response.data[0]["meals"]), 3)

    def test_owner_can_retrieve_health_plan(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("healthplan-detail", args=[self.plan.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.plan.id)
        self.assertEqual(len(response.data["meals"]), 3)
        self.assertEqual(sum(len(meal["items"]) for meal in response.data["meals"]), 9)

    def test_other_user_cannot_retrieve_health_plan(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse("healthplan-detail", args=[self.plan.id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_user_cannot_delete_health_plan(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse("healthplan-detail", args=[self.plan.id]))
        self.plan.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(self.plan.active)

    def test_owner_soft_deletes_health_plan(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("healthplan-detail", args=[self.plan.id]))
        self.plan.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.plan.active)
        self.assertEqual(Meal.objects.filter(health_plan=self.plan).count(), 3)
        self.assertEqual(MealItem.objects.filter(meal__health_plan=self.plan).count(), 9)

        detail_response = self.client.get(reverse("healthplan-detail", args=[self.plan.id]))
        list_response = self.client.get(reverse("healthplan-list"))

        self.assertEqual(detail_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(list_response.data), 0)

    def test_duplicate_plan_date_is_rejected(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("healthplan-generate-meal-plan"), {"plan_date": self.plan_date.isoformat(), "title": "Kế hoạch bị trùng"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["plan_date"], "Ngày này đã có kế hoạch ăn uống.")
        self.assertEqual(HealthPlan.objects.filter(customer=self.user).count(), 1)

    def test_authentication_is_required(self):
        list_response = self.client.get(reverse("healthplan-list"))
        generate_response = self.client.post(reverse("healthplan-generate-meal-plan"), {"plan_date": "2026-08-21"}, format="json")

        self.assertIn(list_response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertIn(generate_response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

class MealPlanGenerationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="generator_customer", email="generator_customer@example.com", password="123456")
        self.health_profile = HealthProfile.objects.create(user=self.user, gender=HealthProfile.Gender.MALE, date_of_birth=date(2004, 5, 10), weight=Decimal("70.00"), height=Decimal("175.00"), activity_level=HealthProfile.ActivityLevel.MODERATE, goal=HealthProfile.Goal.LOSE_WEIGHT)

        self.create_food(1, Food.MealRole.CARBOHYDRATE, "Tinh bột 1")
        self.create_food(2, Food.MealRole.CARBOHYDRATE, "Tinh bột 2")
        self.create_food(3, Food.MealRole.CARBOHYDRATE, "Tinh bột 3")
        self.create_food(4, Food.MealRole.PROTEIN, "Đạm 1")
        self.create_food(5, Food.MealRole.PROTEIN, "Đạm 2")
        self.create_food(6, Food.MealRole.PROTEIN, "Đạm 3")
        self.create_food(7, Food.MealRole.VEGETABLE, "Rau 1")
        self.create_food(8, Food.MealRole.VEGETABLE, "Rau 2")
        self.create_food(9, Food.MealRole.BREAKFAST_SIDE, "Bữa phụ sáng")

    def create_food(self, number, meal_role, category):
        return Food.objects.create(food_id=f"GENERATE{number:04d}", source_name="TEST", name_vi=f"Thực phẩm sinh lịch {number}", name_en=f"Generated food {number}", category_vi=category, category_en=category, item_type=Food.ItemType.COOKED_FOOD, processing_level=Food.ProcessingLevel.MINIMALLY_PROCESSED, meal_role=meal_role, is_meal_suitable=True, kcal_per_100g=Decimal("100.000"), protein_g=Decimal("10.000"), fat_g=Decimal("5.000"), carb_g=Decimal("15.000"), fiber_g=Decimal("2.000"), sodium_mg=Decimal("10.000"), potassium_mg=Decimal("100.000"), saturated_fat_g=Decimal("1.000"))

    def test_generate_one_day_meal_plan(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("healthplan-generate-meal-plan"), {"plan_date": "2026-08-22", "title": "Kế hoạch tự động test"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["health_plan"]["title"], "Kế hoạch tự động test")
        self.assertEqual(response.data["health_plan"]["start_date"], "2026-08-22")
        self.assertEqual(len(response.data["health_plan"]["meals"]), 3)
        self.assertEqual(sum(len(meal["items"]) for meal in response.data["health_plan"]["meals"]), 9)
        self.assertEqual(response.data["attempt_count"], 0)
        self.assertEqual(response.data["evaluation"]["days"][0]["calorie_evaluation"]["status"], "passed")

        plan = HealthPlan.objects.get(customer=self.user, start_date=date(2026, 8, 22))
        self.assertEqual(plan.meals.count(), 3)
        self.assertEqual(MealItem.objects.filter(meal__health_plan=plan).count(), 9)