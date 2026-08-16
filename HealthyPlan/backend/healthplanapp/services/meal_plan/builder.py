from datetime import date
from django.db import transaction
from healthplanapp.models import HealthPlan, Meal, MealItem
from healthplanapp.services.meal_plan.adjuster import adjust_health_plan
from healthplanapp.services.meal_plan.allocation import allocate_meal_calories, calculate_day_portions
from healthplanapp.services.meal_plan.energy import calculate_energy_target
from healthplanapp.services.meal_plan.food_selector import select_day_foods

class OneDayMealPlanBuilder:
    def __init__(self, health_profile, plan_date=None, title="Kế hoạch ăn uống một ngày"):
        self.health_profile = health_profile
        self.plan_date = plan_date or date.today()
        self.title = title
        self.energy_target = None
        self.meal_calorie_targets = None
        self.selected_foods = None
        self.schedule = None
        self.health_plan = None
        self.adjustment_result = None
        self.evaluation = None

    def calculate_targets(self):
        self.energy_target = calculate_energy_target(self.health_profile)
        self.meal_calorie_targets = allocate_meal_calories(self.energy_target["target_calories"])

        return self

    def select_foods(self):
        self.selected_foods = select_day_foods(self.health_profile)

        return self

    def calculate_portions(self):
        self.schedule = calculate_day_portions(self.selected_foods, self.meal_calorie_targets)

        return self

    def create_health_plan(self):
        self.health_plan = HealthPlan.objects.create(customer=self.health_profile.user, title=self.title, plan_type=HealthPlan.PlanType.MEAL, content="", start_date=self.plan_date, end_date=self.plan_date)

        return self

    def create_meals(self):
        for meal_type, meal_schedule in self.schedule.items():
            meal = Meal.objects.create(health_plan=self.health_plan, date=self.plan_date, meal_type=meal_type)
            MealItem.objects.bulk_create([MealItem(meal=meal, food=item["food"], serving_grams=item["serving_grams"]) for item in meal_schedule["items"]])

        return self

    def adjust(self):
        self.adjustment_result = adjust_health_plan(self.health_plan, self.health_profile)
        self.evaluation = self.adjustment_result["evaluation"]

        return self

    @transaction.atomic
    def build(self):
        self.calculate_targets().select_foods().calculate_portions().create_health_plan().create_meals().adjust()

        return {"health_plan": self.health_plan, "energy_target": self.energy_target, "meal_calorie_targets": self.meal_calorie_targets, "schedule": self.schedule, "adjustment_result": self.adjustment_result, "evaluation": self.evaluation}