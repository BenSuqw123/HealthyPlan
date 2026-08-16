from healthplanapp.models import HealthConditionNutrientRule
from healthplanapp.services.meal_plan.nutrition import NUTRIENT_FIELD_MAP
from decimal import Decimal, ROUND_HALF_UP

DAY_NUTRITION_FIELD_MAP = {food_field: result_name for result_name, food_field in NUTRIENT_FIELD_MAP.items()}


class RuleHandler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler

        return handler

    def handle(self, rule, health_profile, day_nutrition):
        if self.next_handler is not None:
            return self.next_handler.handle(rule, health_profile, day_nutrition)

        return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "status": "unsupported", "message": "Chưa có handler phù hợp với rule này."}


class IndividualizedRuleHandler(RuleHandler):
    def handle(self, rule, health_profile, day_nutrition):
        if rule.threshold_unit != "individualized":
            return super().handle(rule, health_profile, day_nutrition)

        return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "needs_expert_review", "recommendation": rule.recommendation_vi, "clinical_caution": rule.clinical_caution_vi}


class DailyAmountRuleHandler(RuleHandler):
    supported_units = {"g/day", "mg/day", "kcal/day"}

    def handle(self, rule, health_profile, day_nutrition):
        if rule.threshold_unit not in self.supported_units:
            return super().handle(rule, health_profile, day_nutrition)

        if day_nutrition is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "status": "unavailable", "message": "Chưa có dữ liệu dinh dưỡng trong ngày."}

        nutrition_field = DAY_NUTRITION_FIELD_MAP.get(rule.evaluation_field)

        if nutrition_field is None:
            return super().handle(rule, health_profile, day_nutrition)

        actual_value = day_nutrition["totals"].get(nutrition_field)
        missing_nutrients = day_nutrition.get("missing_nutrients", [])

        if nutrition_field in missing_nutrients or actual_value is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "unavailable", "message": "Không đủ dữ liệu để đánh giá rule này."}

        if rule.threshold_value is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "needs_expert_review", "recommendation": rule.recommendation_vi, "clinical_caution": rule.clinical_caution_vi}

        if rule.rule_type == HealthConditionNutrientRule.RuleType.LIMIT:
            passed = actual_value <= rule.threshold_value
        elif rule.rule_type == HealthConditionNutrientRule.RuleType.PRIORITIZE:
            passed = actual_value >= rule.threshold_value
        else:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "monitor", "actual_value": actual_value, "threshold_value": rule.threshold_value, "threshold_unit": rule.threshold_unit, "recommendation": rule.recommendation_vi, "clinical_caution": rule.clinical_caution_vi}

        status = "passed" if passed else "failed"

        return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": status, "actual_value": actual_value, "threshold_value": rule.threshold_value, "threshold_unit": rule.threshold_unit, "recommendation": rule.recommendation_vi, "clinical_caution": rule.clinical_caution_vi}


class PercentCaloriesRuleHandler(RuleHandler):
    def handle(self, rule, health_profile, day_nutrition):
        if rule.threshold_unit != "percent_calories":
            return super().handle(rule, health_profile, day_nutrition)

        if day_nutrition is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "status": "unavailable", "message": "Chưa có dữ liệu dinh dưỡng trong ngày."}

        nutrition_field = DAY_NUTRITION_FIELD_MAP.get(rule.evaluation_field)

        if nutrition_field is None:
            return super().handle(rule, health_profile, day_nutrition)

        nutrient_amount = day_nutrition["totals"].get(nutrition_field)
        total_calories = day_nutrition["totals"].get("kcal")
        missing_nutrients = day_nutrition.get("missing_nutrients", [])

        if nutrition_field in missing_nutrients or nutrient_amount is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "unavailable", "message": "Không đủ dữ liệu để đánh giá rule này."}

        if total_calories is None or total_calories <= 0:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "unavailable", "message": "Tổng calorie phải lớn hơn 0."}

        actual_percentage = nutrient_amount * Decimal("9") / total_calories * Decimal("100")
        actual_percentage = actual_percentage.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        if rule.threshold_value is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "needs_expert_review", "recommendation": rule.recommendation_vi, "clinical_caution": rule.clinical_caution_vi}

        if rule.rule_type == HealthConditionNutrientRule.RuleType.LIMIT:
            passed = actual_percentage <= rule.threshold_value
        elif rule.rule_type == HealthConditionNutrientRule.RuleType.PRIORITIZE:
            passed = actual_percentage >= rule.threshold_value
        else:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "monitor", "actual_value": actual_percentage, "threshold_value": rule.threshold_value, "threshold_unit": rule.threshold_unit}

        status = "passed" if passed else "failed"

        return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": status, "actual_value": actual_percentage, "threshold_value": rule.threshold_value, "threshold_unit": rule.threshold_unit, "recommendation": rule.recommendation_vi, "clinical_caution": rule.clinical_caution_vi}
    
class PerKgRuleHandler(RuleHandler):
    def handle(self, rule, health_profile, day_nutrition):
        if rule.threshold_unit != "g/kg/day":
            return super().handle(rule, health_profile, day_nutrition)

        if day_nutrition is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "status": "unavailable", "message": "Chưa có dữ liệu dinh dưỡng trong ngày."}

        if health_profile.weight is None or health_profile.weight <= 0:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "status": "unavailable", "message": "Cân nặng trong hồ sơ sức khỏe không hợp lệ."}

        nutrition_field = DAY_NUTRITION_FIELD_MAP.get(rule.evaluation_field)

        if nutrition_field is None:
            return super().handle(rule, health_profile, day_nutrition)

        actual_value = day_nutrition["totals"].get(nutrition_field)
        missing_nutrients = day_nutrition.get("missing_nutrients", [])

        if nutrition_field in missing_nutrients or actual_value is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "unavailable", "message": "Không đủ dữ liệu để đánh giá rule này."}

        if rule.threshold_value is None:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "needs_expert_review", "recommendation": rule.recommendation_vi, "clinical_caution": rule.clinical_caution_vi}

        daily_threshold = rule.threshold_value * health_profile.weight

        if rule.rule_type == HealthConditionNutrientRule.RuleType.LIMIT:
            passed = actual_value <= daily_threshold
        elif rule.rule_type == HealthConditionNutrientRule.RuleType.PRIORITIZE:
            passed = actual_value >= daily_threshold
        else:
            return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": "monitor", "actual_value": actual_value, "threshold_value": daily_threshold, "threshold_unit": "g/day"}

        status = "passed" if passed else "failed"

        return {"rule_id": rule.rule_id, "condition_code": rule.condition_code, "evaluation_field": rule.evaluation_field, "status": status, "actual_value": actual_value, "threshold_value": daily_threshold, "threshold_unit": "g/day", "source_threshold_value": rule.threshold_value, "source_threshold_unit": rule.threshold_unit, "recommendation": rule.recommendation_vi, "clinical_caution": rule.clinical_caution_vi}

def build_rule_handler_chain():
    individualized_handler = IndividualizedRuleHandler()
    daily_amount_handler = DailyAmountRuleHandler()
    percent_calories_handler = PercentCaloriesRuleHandler()
    per_kg_handler = PerKgRuleHandler()

    individualized_handler.set_next(daily_amount_handler).set_next(percent_calories_handler).set_next(per_kg_handler)

    return individualized_handler