from decimal import Decimal, ROUND_HALF_UP


NUTRIENT_FIELD_MAP = {"kcal": "kcal_per_100g", "protein_g": "protein_g", "fat_g": "fat_g", "carb_g": "carb_g", "fiber_g": "fiber_g", "sodium_mg": "sodium_mg", "potassium_mg": "potassium_mg", "saturated_fat_g": "saturated_fat_g"}


def calculate_nutrient(value, serving_grams):
    if value is None:
        return None

    result = value * serving_grams / Decimal("100")

    return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_meal_item_nutrition(meal_item):
    food = meal_item.food
    nutrition = {"food_id": food.food_id, "food_name": food.name_vi, "serving_grams": meal_item.serving_grams}

    for result_name, food_field in NUTRIENT_FIELD_MAP.items():
        value_per_100g = getattr(food, food_field)
        nutrition[result_name] = calculate_nutrient(value_per_100g, meal_item.serving_grams)

    return nutrition

def calculate_meal_nutrition(meal):
    totals = {name: Decimal("0.00") for name in NUTRIENT_FIELD_MAP}
    missing_nutrients = set()
    items = []

    meal_items = meal.items.filter(active=True).select_related("food")

    for meal_item in meal_items:
        item_nutrition = calculate_meal_item_nutrition(meal_item)
        items.append(item_nutrition)

        for nutrient_name in NUTRIENT_FIELD_MAP:
            value = item_nutrition[nutrient_name]

            if value is None:
                missing_nutrients.add(nutrient_name)
                continue

            totals[nutrient_name] += value

    return {"meal_id": meal.id, "date": meal.date, "meal_type": meal.meal_type, "meal_type_display": meal.get_meal_type_display(),
     "items": items, "totals": totals, "missing_nutrients": sorted(missing_nutrients)}

def calculate_health_plan_nutrition(health_plan):
    days = {}
    meal_order = {"breakfast": 1, "lunch": 2, "dinner": 3}
    meals = health_plan.meals.filter(active=True)
    meals = sorted(meals, key=lambda meal: (meal.date, meal_order.get(meal.meal_type, 99)))

    for meal in meals:
        meal_nutrition = calculate_meal_nutrition(meal)
        date_key = meal.date.isoformat()

        if date_key not in days:
            days[date_key] = {"date": meal.date, "meals": [], "totals": {name: Decimal("0.00") for name in NUTRIENT_FIELD_MAP}, "missing_nutrients": set()}

        day = days[date_key]
        day["meals"].append(meal_nutrition)

        for nutrient_name in NUTRIENT_FIELD_MAP:
            day["totals"][nutrient_name] += meal_nutrition["totals"][nutrient_name]

        day["missing_nutrients"].update(meal_nutrition["missing_nutrients"])

    for day in days.values():
        day["missing_nutrients"] = sorted(day["missing_nutrients"])

    return {"health_plan_id": health_plan.id, "days": list(days.values())}