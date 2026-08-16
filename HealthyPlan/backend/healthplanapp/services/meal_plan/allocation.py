from decimal import Decimal, ROUND_HALF_UP

MEAL_CALORIE_RATIOS = {"breakfast": Decimal("0.25"), "lunch": Decimal("0.40"), "dinner": Decimal("0.35")}
MEAL_ROLE_CALORIE_RATIOS = {"breakfast": {"carbohydrate": Decimal("0.40"), "protein": Decimal("0.30"), "breakfast_side": Decimal("0.30")}, "lunch": {"carbohydrate": Decimal("0.40"), "protein": Decimal("0.35"), "vegetable": Decimal("0.25")}, "dinner": {"carbohydrate": Decimal("0.40"), "protein": Decimal("0.35"), "vegetable": Decimal("0.25")}}
SERVING_GRAM_RANGES = {"carbohydrate": (Decimal("50"), Decimal("350")), "protein": (Decimal("50"), Decimal("200")), "vegetable": (Decimal("100"), Decimal("250")), "breakfast_side": (Decimal("100"), Decimal("250"))}
SERVING_ADJUSTMENT_ORDER = ["carbohydrate", "protein", "breakfast_side", "vegetable"]

def allocate_meal_calories(target_calories):
    target_calories = Decimal(str(target_calories))

    if target_calories <= 0:
        raise ValueError("Calories mục tiêu phải lớn hơn 0.")

    breakfast_calories = (target_calories * MEAL_CALORIE_RATIOS["breakfast"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    lunch_calories = (target_calories * MEAL_CALORIE_RATIOS["lunch"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    dinner_calories = target_calories - breakfast_calories - lunch_calories

    return {"breakfast": breakfast_calories, "lunch": lunch_calories, "dinner": dinner_calories}

def clamp_serving_grams(serving_grams, food_role):
    minimum_grams, maximum_grams = SERVING_GRAM_RANGES[food_role]
    serving_grams = max(minimum_grams, min(serving_grams, maximum_grams))

    return serving_grams.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def calculate_food_calories(food, serving_grams):
    calories = food.kcal_per_100g * serving_grams / Decimal("100")

    return calories.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def calculate_meal_portions(meal_type, selected_foods, target_calories):
    target_calories = Decimal(str(target_calories))
    role_ratios = MEAL_ROLE_CALORIE_RATIOS[meal_type]
    items = []

    for selected_food in selected_foods:
        food_role = str(selected_food["role"])
        food = selected_food["food"]
        allocated_calories = target_calories * role_ratios[food_role]
        serving_grams = allocated_calories * Decimal("100") / food.kcal_per_100g
        serving_grams = clamp_serving_grams(serving_grams, food_role)
        items.append({"role": food_role, "food": food, "serving_grams": serving_grams})

    for food_role in SERVING_ADJUSTMENT_ORDER:
        item = next((item for item in items if item["role"] == food_role), None)

        if item is None:
            continue

        actual_calories = sum((calculate_food_calories(item["food"], item["serving_grams"]) for item in items), Decimal("0"))
        calorie_difference = target_calories - actual_calories

        if abs(calorie_difference) <= Decimal("0.50"):
            break

        adjusted_grams = item["serving_grams"] + calorie_difference * Decimal("100") / item["food"].kcal_per_100g
        item["serving_grams"] = clamp_serving_grams(adjusted_grams, food_role)

    actual_calories = sum((calculate_food_calories(item["food"], item["serving_grams"]) for item in items), Decimal("0"))

    for item in items:
        item["calories"] = calculate_food_calories(item["food"], item["serving_grams"])

    return {"meal_type": meal_type, "target_calories": target_calories, "actual_calories": actual_calories, "items": items}

def calculate_day_portions(selected_foods, meal_calorie_targets):
    return {meal_type: calculate_meal_portions(meal_type, items, meal_calorie_targets[meal_type]) for meal_type, items in selected_foods.items()}