from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

from healthplanapp.models import HealthProfile


class MealPlanStrategy(ABC):
    @abstractmethod
    def calculate_target_calories(self, tdee):
        pass


class WeightLossStrategy(MealPlanStrategy):
    def calculate_target_calories(self, tdee):
        target_calories = max(tdee - Decimal("500"), Decimal("1200"))

        return target_calories.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class WeightMaintenanceStrategy(MealPlanStrategy):
    def calculate_target_calories(self, tdee):
        return tdee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class WeightGainStrategy(MealPlanStrategy):
    def calculate_target_calories(self, tdee):
        target_calories = tdee + Decimal("300")

        return target_calories.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


STRATEGY_MAP = {HealthProfile.Goal.LOSE_WEIGHT: WeightLossStrategy, HealthProfile.Goal.MAINTAIN_WEIGHT: WeightMaintenanceStrategy, HealthProfile.Goal.GAIN_WEIGHT: WeightGainStrategy}


def get_meal_plan_strategy(goal):
    strategy_class = STRATEGY_MAP.get(goal)

    if strategy_class is None:
        raise ValueError(f"Mục tiêu sức khỏe không hợp lệ: {goal}")

    return strategy_class()