from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from healthplanapp.models import HealthConditionNutrientRule, MealItem
from healthplanapp.services.meal_plan.allocation import clamp_serving_grams
from healthplanapp.services.meal_plan.food_selector import RULE_PRIORITY_ORDER, get_ranked_food_candidates
from healthplanapp.services.meal_plan.nutrition import NUTRIENT_FIELD_MAP
from healthplanapp.services.meal_plan.plan_evaluator import evaluate_calorie_target, evaluate_health_plan
from healthplanapp.services.meal_plan.rule_evaluator import evaluate_day_rules

TARGETED_CANDIDATE_LIMIT = 10

def calculate_food_nutrients(food, serving_grams):
    nutrients = {}

    for result_field, food_field in NUTRIENT_FIELD_MAP.items():
        value = getattr(food, food_field)

        if value is None:
            nutrients[result_field] = None
        else:
            nutrients[result_field] = (value * serving_grams / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return nutrients

def preview_meal_item_replacement(meal_item, new_food, health_profile, day_nutrition, target_calories):
    food_role = meal_item.food.meal_role

    if new_food.meal_role != food_role:
        raise ValueError("Food thay thế phải có cùng meal_role.")

    old_nutrients = calculate_food_nutrients(meal_item.food, meal_item.serving_grams)
    old_calories = old_nutrients["kcal"]
    new_serving_grams = old_calories * Decimal("100") / new_food.kcal_per_100g
    new_serving_grams = clamp_serving_grams(new_serving_grams, food_role)
    new_nutrients = calculate_food_nutrients(new_food, new_serving_grams)
    projected_totals = dict(day_nutrition["totals"])

    for nutrient_field in NUTRIENT_FIELD_MAP:
        old_value = old_nutrients[nutrient_field]
        new_value = new_nutrients[nutrient_field]
        current_total = projected_totals.get(nutrient_field)

        if old_value is not None and new_value is not None and current_total is not None:
            projected_totals[nutrient_field] = (current_total - old_value + new_value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    projected_day_nutrition = dict(day_nutrition)
    projected_day_nutrition["totals"] = projected_totals
    rule_evaluation = evaluate_day_rules(health_profile, projected_day_nutrition)
    calorie_evaluation = evaluate_calorie_target(projected_totals["kcal"], target_calories)

    return {"meal_item_id": meal_item.id, "old_food": meal_item.food, "new_food": new_food, "old_serving_grams": meal_item.serving_grams, "new_serving_grams": new_serving_grams, "old_calories": old_calories, "new_calories": new_nutrients["kcal"], "projected_day_nutrition": projected_day_nutrition, "rule_evaluation": rule_evaluation, "calorie_evaluation": calorie_evaluation}

def has_adjustment_conflict(day_evaluation, failed_rule):
    increase_rule_types = {HealthConditionNutrientRule.RuleType.PRIORITIZE}
    decrease_rule_types = {HealthConditionNutrientRule.RuleType.LIMIT, HealthConditionNutrientRule.RuleType.AVOID, HealthConditionNutrientRule.RuleType.MODERATE}
    target_rule_type = failed_rule["rule_type"]

    for rule in day_evaluation["results"]:
        if rule["rule_id"] == failed_rule["rule_id"] or rule["evaluation_field"] != failed_rule["evaluation_field"]:
            continue

        if rule["status"] == "needs_expert_review":
            return True

        if target_rule_type in increase_rule_types and rule["rule_type"] in decrease_rule_types:
            return True

        if target_rule_type in decrease_rule_types and rule["rule_type"] in increase_rule_types:
            return True

    return False

def get_targeted_candidates(health_profile, food_role, evaluation_field, rule_type, excluded_food_ids):
    candidates = list(get_ranked_food_candidates(health_profile, food_role).exclude(id__in=excluded_food_ids))
    reverse = rule_type == HealthConditionNutrientRule.RuleType.PRIORITIZE
    candidates.sort(key=lambda food: getattr(food, evaluation_field) / food.kcal_per_100g, reverse=reverse)

    return candidates[:TARGETED_CANDIDATE_LIMIT]

def find_best_replacement(health_plan, health_profile, evaluation, failed_rule):
    day_evaluation = evaluation["days"][0]

    if has_adjustment_conflict(day_evaluation, failed_rule):
        return None

    evaluation_field = failed_rule["evaluation_field"]
    current_failed_rule_ids = {rule["rule_id"] for rule in day_evaluation["results"] if rule["status"] == "failed"}
    used_food_ids = set(MealItem.objects.filter(meal__health_plan=health_plan).values_list("food_id", flat=True))
    meal_items = MealItem.objects.filter(meal__health_plan=health_plan, meal__date=day_evaluation["date"]).select_related("food", "meal")
    best_preview = None
    best_score = None

    for meal_item in meal_items:
        candidates = get_targeted_candidates(health_profile, meal_item.food.meal_role, evaluation_field, failed_rule["rule_type"], used_food_ids)

        for candidate in candidates:
            preview = preview_meal_item_replacement(meal_item, candidate, health_profile, day_evaluation["nutrition"], evaluation["energy_target"]["target_calories"])

            if preview["calorie_evaluation"]["status"] != "passed":
                continue

            projected_results = preview["rule_evaluation"]["results"]
            projected_failed_rule_ids = {rule["rule_id"] for rule in projected_results if rule["status"] == "failed"}
            new_failed_rule_ids = projected_failed_rule_ids - current_failed_rule_ids

            if new_failed_rule_ids:
                continue

            projected_rule = next(rule for rule in projected_results if rule["rule_id"] == failed_rule["rule_id"])
            projected_actual_value = projected_rule.get("actual_value")

            if projected_actual_value is None:
                continue

            if failed_rule["rule_type"] == HealthConditionNutrientRule.RuleType.PRIORITIZE:
                improvement = projected_actual_value - failed_rule["actual_value"]
            else:
                improvement = failed_rule["actual_value"] - projected_actual_value

            if improvement <= 0:
                continue

            target_passed = projected_rule["status"] == "passed"
            calorie_difference = abs(preview["calorie_evaluation"]["actual_calories"] - preview["calorie_evaluation"]["target_calories"])
            item_type_priority = candidate.item_type_priority

            if target_passed and failed_rule["threshold_value"] is not None:
                threshold_difference = abs(projected_actual_value - failed_rule["threshold_value"])
                score = (1, -item_type_priority, -threshold_difference, -calorie_difference)
            else:
                score = (0, improvement, -item_type_priority, -calorie_difference)

            if best_score is None or score > best_score:
                best_score = score
                best_preview = preview

    return best_preview

@transaction.atomic
def apply_previewed_replacement(preview):
    meal_item = MealItem.objects.select_for_update().get(id=preview["meal_item_id"])

    if meal_item.food_id != preview["old_food"].id or meal_item.serving_grams != preview["old_serving_grams"]:
        raise ValueError("MealItem đã thay đổi sau khi tạo preview.")

    meal_item.food = preview["new_food"]
    meal_item.serving_grams = preview["new_serving_grams"]
    meal_item.save(update_fields=["food", "serving_grams", "updated_date"])

    return meal_item

def adjust_health_plan(health_plan, health_profile, max_attempts=5):
    adjustment_history = []

    for attempt in range(1, max_attempts + 1):
        evaluation = evaluate_health_plan(health_plan, health_profile)
        failed_rules = [rule for day in evaluation["days"] for rule in day["results"] if rule["status"] == "failed"]

        if not failed_rules:
            break

        failed_rules.sort(key=lambda rule: RULE_PRIORITY_ORDER.get(rule["priority"], 3))
        failed_rule = failed_rules[0]
        preview = find_best_replacement(health_plan, health_profile, evaluation, failed_rule)

        if preview is None:
            break

        apply_previewed_replacement(preview)
        adjustment_history.append({"attempt": attempt, "rule_id": failed_rule["rule_id"], "old_food": preview["old_food"].name_vi, "new_food": preview["new_food"].name_vi, "old_serving_grams": preview["old_serving_grams"], "new_serving_grams": preview["new_serving_grams"]})

    final_evaluation = evaluate_health_plan(health_plan, health_profile)

    return {"status": final_evaluation["status"], "attempt_count": len(adjustment_history), "adjustments": adjustment_history, "evaluation": final_evaluation}