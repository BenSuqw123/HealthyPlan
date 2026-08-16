from healthplanapp.models import HealthConditionNutrientRule, HealthProfile


GENERAL_CONDITION_CODE = "general_healthy_adult"


def get_profile_condition_codes(health_profile):
    condition_codes = set(health_profile.health_issues.filter(active=True).values_list("code", flat=True))
    condition_codes.add(GENERAL_CONDITION_CODE)

    return sorted(condition_codes)


def get_applicable_rules(health_profile):
    condition_codes = get_profile_condition_codes(health_profile)
    rules = HealthConditionNutrientRule.objects.filter(active=True, condition_code__in=condition_codes)

    if health_profile.goal != HealthProfile.Goal.LOSE_WEIGHT:
        rules = rules.exclude(applies_when="weight_loss_goal")

    return rules.order_by("condition_code", "rule_id")

def resolve_rule_precedence(rules):
    rules = list(rules)
    specific_fields = {rule.evaluation_field for rule in rules if rule.condition_code != GENERAL_CONDITION_CODE}

    return [rule for rule in rules if rule.condition_code != GENERAL_CONDITION_CODE or rule.evaluation_field not in specific_fields]


def get_effective_rules(health_profile):
    rules = get_applicable_rules(health_profile)

    return resolve_rule_precedence(rules)