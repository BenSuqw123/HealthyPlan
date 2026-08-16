from django.db.models import Case, F, IntegerField, Value, When
from healthplanapp.models import Food, HealthConditionNutrientRule
from healthplanapp.services.meal_plan.health_rules import get_effective_rules
from healthplanapp.services.meal_plan.nutrition import NUTRIENT_FIELD_MAP

RULE_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
SUPPORTED_FOOD_FIELDS = set(NUTRIENT_FIELD_MAP.values())

MEAL_ROLE_ITEM_TYPE_MAP = {Food.MealRole.CARBOHYDRATE: [Food.ItemType.COOKED_FOOD, Food.ItemType.BASIC_FOOD], Food.MealRole.PROTEIN: [Food.ItemType.COOKED_FOOD, Food.ItemType.BASIC_FOOD], Food.MealRole.VEGETABLE: [Food.ItemType.COOKED_FOOD, Food.ItemType.BASIC_FOOD], Food.MealRole.BREAKFAST_SIDE: [Food.ItemType.BASIC_FOOD, Food.ItemType.RAW_INGREDIENT, Food.ItemType.BEVERAGE, Food.ItemType.COOKED_FOOD]}
MEAL_ROLE_KCAL_RANGE_MAP = {Food.MealRole.CARBOHYDRATE: (50, 250), Food.MealRole.PROTEIN: (50, 300), Food.MealRole.VEGETABLE: (10, 150), Food.MealRole.BREAKFAST_SIDE: (20, 200)}
MEAL_FOOD_ROLE_MAP = {"breakfast": [Food.MealRole.CARBOHYDRATE, Food.MealRole.PROTEIN, Food.MealRole.BREAKFAST_SIDE], "lunch": [Food.MealRole.CARBOHYDRATE, Food.MealRole.PROTEIN, Food.MealRole.VEGETABLE], "dinner": [Food.MealRole.CARBOHYDRATE, Food.MealRole.PROTEIN, Food.MealRole.VEGETABLE]}

def get_food_candidates_by_role(food_role):
    allowed_item_types = MEAL_ROLE_ITEM_TYPE_MAP.get(food_role)

    if allowed_item_types is None:
        raise ValueError(f"Vai trò thực phẩm không hợp lệ: {food_role}")

    minimum_kcal, maximum_kcal = MEAL_ROLE_KCAL_RANGE_MAP[food_role]
    item_type_priority = Case(*[When(item_type=item_type, then=Value(index)) for index, item_type in enumerate(allowed_item_types)], default=Value(len(allowed_item_types)), output_field=IntegerField())

    return Food.objects.filter(active=True, is_meal_suitable=True, meal_role=food_role, item_type__in=allowed_item_types, kcal_per_100g__gte=minimum_kcal, kcal_per_100g__lte=maximum_kcal, processing_level__in=[Food.ProcessingLevel.UNPROCESSED, Food.ProcessingLevel.MINIMALLY_PROCESSED]).annotate(item_type_priority=item_type_priority)

def get_food_ranking_rules(health_profile):
    rules = sorted(get_effective_rules(health_profile), key=lambda rule: RULE_PRIORITY_ORDER.get(rule.priority, 3))
    ranking_rules = []
    used_fields = set()

    for rule in rules:
        field = rule.evaluation_field

        if rule.threshold_unit == "individualized" or field not in SUPPORTED_FOOD_FIELDS or field in used_fields:
            continue

        if rule.rule_type in {HealthConditionNutrientRule.RuleType.LIMIT, HealthConditionNutrientRule.RuleType.AVOID, HealthConditionNutrientRule.RuleType.MODERATE, HealthConditionNutrientRule.RuleType.PRIORITIZE}:
            ranking_rules.append(rule)
            used_fields.add(field)

    return ranking_rules

def get_food_rule_ordering(ranking_rules):
    ordering = []

    for rule in ranking_rules:
        if rule.rule_type in {HealthConditionNutrientRule.RuleType.LIMIT, HealthConditionNutrientRule.RuleType.AVOID, HealthConditionNutrientRule.RuleType.MODERATE}:
            ordering.append(F(rule.evaluation_field).asc(nulls_last=True))
        elif rule.rule_type == HealthConditionNutrientRule.RuleType.PRIORITIZE:
            ordering.append(F(rule.evaluation_field).desc(nulls_last=True))

    return ordering

def get_ranked_food_candidates(health_profile, food_role):
    foods = get_food_candidates_by_role(food_role)
    ranking_rules = get_food_ranking_rules(health_profile)

    for rule in ranking_rules:
        foods = foods.filter(**{f"{rule.evaluation_field}__isnull": False})

    ordering = get_food_rule_ordering(ranking_rules)

    return foods.order_by("item_type_priority", *ordering, "name_vi")

def select_food_candidate(health_profile, food_role, excluded_food_ids=None, excluded_categories=None):
    excluded_food_ids = excluded_food_ids or set()
    excluded_categories = excluded_categories or set()
    foods = get_ranked_food_candidates(health_profile, food_role).exclude(id__in=excluded_food_ids)

    if excluded_categories:
        foods = foods.exclude(category_vi__in=excluded_categories)

    food = foods.first()

    if food is None:
        raise ValueError(f"Không tìm thấy Food phù hợp cho role: {food_role}")

    return food

def select_day_foods(health_profile):
    selected_foods = {}
    excluded_food_ids = set()
    used_protein_categories = set()

    for meal_type, food_roles in MEAL_FOOD_ROLE_MAP.items():
        selected_foods[meal_type] = []

        for food_role in food_roles:
            excluded_categories = used_protein_categories if food_role == Food.MealRole.PROTEIN else set()
            food = select_food_candidate(health_profile, food_role, excluded_food_ids, excluded_categories)
            selected_foods[meal_type].append({"role": food_role, "food": food})
            excluded_food_ids.add(food.id)

            if food_role == Food.MealRole.PROTEIN:
                used_protein_categories.add(food.category_vi)

    return selected_foods