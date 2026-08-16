from decimal import Decimal, ROUND_HALF_UP
from healthplanapp.services.meal_plan.energy import calculate_energy_target
from healthplanapp.services.meal_plan.nutrition import calculate_health_plan_nutrition
from healthplanapp.services.meal_plan.rule_evaluator import evaluate_day_rules

CALORIE_TOLERANCE_RATIO = Decimal("0.10")

def evaluate_calorie_target(actual_calories, target_calories):
    if actual_calories is None:
        return {"status": "unavailable", "message": "Không có dữ liệu calories để đánh giá."}

    actual_calories = Decimal(str(actual_calories)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    target_calories = Decimal(str(target_calories)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    minimum_calories = (target_calories * (Decimal("1") - CALORIE_TOLERANCE_RATIO)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    maximum_calories = (target_calories * (Decimal("1") + CALORIE_TOLERANCE_RATIO)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if actual_calories < minimum_calories:
        status = "below_target"
    elif actual_calories > maximum_calories:
        status = "above_target"
    else:
        status = "passed"

    return {"status": status, "actual_calories": actual_calories, "target_calories": target_calories, "minimum_calories": minimum_calories, "maximum_calories": maximum_calories}

def get_health_plan_status(day_evaluations):
    if not day_evaluations:
        return "empty_plan"

    statuses = {day["status"] for day in day_evaluations}

    if "needs_adjustment" in statuses:
        return "needs_adjustment"

    if "needs_expert_review" in statuses:
        return "needs_expert_review"

    if "incomplete_data" in statuses:
        return "incomplete_data"

    if statuses == {"no_rules"}:
        return "no_rules"

    return "passed"

def evaluate_health_plan(health_plan, health_profile):
    energy_target = calculate_energy_target(health_profile)
    plan_nutrition = calculate_health_plan_nutrition(health_plan)
    day_evaluations = []

    for day_nutrition in plan_nutrition["days"]:
        evaluation = evaluate_day_rules(health_profile, day_nutrition)
        actual_calories = day_nutrition.get("totals", {}).get("kcal")
        calorie_evaluation = evaluate_calorie_target(actual_calories, energy_target["target_calories"])

        if calorie_evaluation["status"] in {"below_target", "above_target"}:
            evaluation["status"] = "needs_adjustment"
        elif calorie_evaluation["status"] == "unavailable" and evaluation["status"] not in {"needs_adjustment", "needs_expert_review"}:
            evaluation["status"] = "incomplete_data"

        evaluation["calorie_evaluation"] = calorie_evaluation
        evaluation["nutrition"] = day_nutrition
        day_evaluations.append(evaluation)

    status = get_health_plan_status(day_evaluations)

    return {"health_plan_id": health_plan.id, "status": status, "day_count": len(day_evaluations), "energy_target": energy_target, "days": day_evaluations}