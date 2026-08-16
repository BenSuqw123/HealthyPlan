from healthplanapp.services.meal_plan.health_rules import get_effective_rules
from healthplanapp.services.meal_plan.rule_handlers import build_rule_handler_chain


def get_day_rule_status(results):
    if not results:
        return "no_rules"

    statuses = {result["status"] for result in results}

    if "failed" in statuses:
        return "needs_adjustment"

    if "needs_expert_review" in statuses:
        return "needs_expert_review"

    if "unavailable" in statuses or "unsupported" in statuses:
        return "incomplete_data"

    return "passed"


def evaluate_day_rules(health_profile, day_nutrition):
    rules = get_effective_rules(health_profile)
    handler_chain = build_rule_handler_chain()
    results = []

    for rule in rules:
        result = handler_chain.handle(rule, health_profile, day_nutrition)
        result["rule_type"] = rule.rule_type
        result["priority"] = rule.priority
        results.append(result)

    status = get_day_rule_status(results)

    return {"date": day_nutrition.get("date"), "status": status, "rule_count": len(results), "results": results}