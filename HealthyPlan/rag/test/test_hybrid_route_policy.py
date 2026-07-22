from hybrid_condition_router import build_multilabel_route_fields, resolve_route_decision


def create_entity_result(condition_codes):
    matches = []

    for condition_code in condition_codes:
        matches.append(
            {
                "condition_code": condition_code,
                "matched_text": condition_code,
                "match_type": "test_entity",
            }
        )

    return {
        "condition_codes": condition_codes,
        "matches": matches,
    }


def create_safety_result(safety_flags):
    matches = []

    for safety_flag in safety_flags:
        matches.append(
            {
                "flag_code": safety_flag,
                "matched_text": safety_flag,
                "match_type": "test_safety_flag",
            }
        )

    return {
        "safety_flags": safety_flags,
        "matches": matches,
    }


route_decision_test_cases = [
    {
        "name": "explicit diabetes type 1 overrides ambiguous hybrid result",
        "status": "ambiguous",
        "condition_code": None,
        "condition_codes": ["diabetes_type_1"],
        "safety_flags": [],
        "expected_status": "detected",
        "expected_condition_code": "diabetes_type_1",
        "expected_decision_reason": "explicit_entity_override",
    },
    {
        "name": "explicit CKD G3b overrides ambiguous hybrid result",
        "status": "ambiguous",
        "condition_code": None,
        "condition_codes": ["ckd_g3b"],
        "safety_flags": [],
        "expected_status": "detected",
        "expected_condition_code": "ckd_g3b",
        "expected_decision_reason": "explicit_entity_override",
    },
    {
        "name": "pregnancy routes to general safety",
        "status": "detected",
        "condition_code": "diabetes_type_2",
        "condition_codes": ["diabetes_type_2"],
        "safety_flags": ["pregnancy"],
        "expected_status": "detected",
        "expected_condition_code": "general_safety",
        "expected_decision_reason": "safety_flag_override",
    },
    {
        "name": "elderly frailty routes to general safety",
        "status": "detected",
        "condition_code": "obesity",
        "condition_codes": ["obesity"],
        "safety_flags": ["elderly_frailty", "malnutrition_risk"],
        "expected_status": "detected",
        "expected_condition_code": "general_safety",
        "expected_decision_reason": "safety_flag_override",
    },
    {
        "name": "conflicting diet rules route to general safety",
        "status": "ambiguous",
        "condition_code": None,
        "condition_codes": ["ckd_g4", "obesity"],
        "safety_flags": ["multiple_conditions", "conflicting_diet_rules"],
        "expected_status": "detected",
        "expected_condition_code": "general_safety",
        "expected_decision_reason": "safety_flag_override",
    },
    {
        "name": "inconsistent laboratory values route to general safety",
        "status": "detected",
        "condition_code": "ckd_stage_unknown",
        "condition_codes": [],
        "safety_flags": ["inconsistent_lab_results"],
        "expected_status": "detected",
        "expected_condition_code": "general_safety",
        "expected_decision_reason": "safety_flag_override",
    },
    {
        "name": "self medication risk routes to general safety",
        "status": "detected",
        "condition_code": "diabetes_type_2",
        "condition_codes": ["diabetes_type_2"],
        "safety_flags": ["medication_risk"],
        "expected_status": "detected",
        "expected_condition_code": "general_safety",
        "expected_decision_reason": "safety_flag_override",
    },
    {
        "name": "emergency symptom routes to general safety",
        "status": "unknown",
        "condition_code": None,
        "condition_codes": [],
        "safety_flags": ["possible_emergency"],
        "expected_status": "detected",
        "expected_condition_code": "general_safety",
        "expected_decision_reason": "safety_flag_override",
    },
    {
        "name": "multiple conditions alone do not force safety route",
        "status": "detected",
        "condition_code": "diabetes_type_2",
        "condition_codes": ["obesity", "diabetes_type_2"],
        "safety_flags": ["multiple_conditions"],
        "expected_status": "detected",
        "expected_condition_code": "diabetes_type_2",
        "expected_decision_reason": "hybrid_router",
    },
    {
        "name": "hybrid result remains when there is no explicit entity",
        "status": "detected",
        "condition_code": "hypertension",
        "condition_codes": [],
        "safety_flags": [],
        "expected_status": "detected",
        "expected_condition_code": "hypertension",
        "expected_decision_reason": "hybrid_router",
    },
    {
        "name": "unknown remains unknown without entity or safety evidence",
        "status": "unknown",
        "condition_code": None,
        "condition_codes": [],
        "safety_flags": [],
        "expected_status": "unknown",
        "expected_condition_code": None,
        "expected_decision_reason": "hybrid_router",
    },
]


for test_index, test_case in enumerate(route_decision_test_cases, start=1):
    entity_result = create_entity_result(test_case["condition_codes"])
    safety_result = create_safety_result(test_case["safety_flags"])

    route_decision = resolve_route_decision(
        test_case["status"],
        test_case["condition_code"],
        entity_result,
        safety_result,
    )

    assert route_decision["status"] == test_case["expected_status"], (
        f"Route decision test #{test_index} failed\n"
        f"Name: {test_case['name']}\n"
        f"Expected status: {test_case['expected_status']}\n"
        f"Actual status: {route_decision['status']}"
    )

    assert route_decision["condition_code"] == test_case["expected_condition_code"], (
        f"Route decision test #{test_index} failed\n"
        f"Name: {test_case['name']}\n"
        f"Expected condition: {test_case['expected_condition_code']}\n"
        f"Actual condition: {route_decision['condition_code']}"
    )

    assert route_decision["decision_reason"] == test_case["expected_decision_reason"], (
        f"Route decision test #{test_index} failed\n"
        f"Name: {test_case['name']}\n"
        f"Expected reason: {test_case['expected_decision_reason']}\n"
        f"Actual reason: {route_decision['decision_reason']}"
    )


multilabel_field_test_cases = [
    {
        "name": "detected route exposes its primary condition",
        "status": "detected",
        "condition_code": "ckd_g4",
        "condition_codes": ["ckd_g4"],
        "safety_flags": [],
        "expected_conditions": ["ckd_g4"],
        "expected_primary_condition": "ckd_g4",
        "expected_primary_route": "condition",
        "expected_needs_clarification": False,
    },
    {
        "name": "hybrid condition is inserted when entity extractor has no condition",
        "status": "detected",
        "condition_code": "hypertension",
        "condition_codes": [],
        "safety_flags": [],
        "expected_conditions": ["hypertension"],
        "expected_primary_condition": "hypertension",
        "expected_primary_route": "condition",
        "expected_needs_clarification": False,
    },
    {
        "name": "multi-label conditions remain available",
        "status": "detected",
        "condition_code": "diabetes_type_2",
        "condition_codes": ["obesity", "diabetes_type_2"],
        "safety_flags": ["multiple_conditions"],
        "expected_conditions": ["obesity", "diabetes_type_2"],
        "expected_primary_condition": "diabetes_type_2",
        "expected_primary_route": "condition",
        "expected_needs_clarification": False,
    },
    {
        "name": "general safety has no primary medical condition",
        "status": "detected",
        "condition_code": "general_safety",
        "condition_codes": ["ckd_g4", "obesity"],
        "safety_flags": ["multiple_conditions", "conflicting_diet_rules"],
        "expected_conditions": ["ckd_g4", "obesity"],
        "expected_primary_condition": None,
        "expected_primary_route": "general_safety",
        "expected_needs_clarification": False,
    },
    {
        "name": "ambiguous route needs clarification",
        "status": "ambiguous",
        "condition_code": None,
        "condition_codes": [],
        "safety_flags": [],
        "expected_conditions": [],
        "expected_primary_condition": None,
        "expected_primary_route": "clarification",
        "expected_needs_clarification": True,
    },
    {
        "name": "unknown route needs clarification",
        "status": "unknown",
        "condition_code": None,
        "condition_codes": [],
        "safety_flags": [],
        "expected_conditions": [],
        "expected_primary_condition": None,
        "expected_primary_route": "unknown",
        "expected_needs_clarification": True,
    },
]


for test_index, test_case in enumerate(multilabel_field_test_cases, start=1):
    entity_result = create_entity_result(test_case["condition_codes"])
    safety_result = create_safety_result(test_case["safety_flags"])

    route_fields = build_multilabel_route_fields(
        test_case["status"],
        test_case["condition_code"],
        entity_result,
        safety_result,
    )

    assert route_fields["conditions"] == test_case["expected_conditions"], (
        f"Multi-label field test #{test_index} failed\n"
        f"Name: {test_case['name']}\n"
        f"Expected conditions: {test_case['expected_conditions']}\n"
        f"Actual conditions: {route_fields['conditions']}"
    )

    assert route_fields["safety_flags"] == test_case["safety_flags"], (
        f"Multi-label field test #{test_index} failed\n"
        f"Name: {test_case['name']}\n"
        f"Expected safety flags: {test_case['safety_flags']}\n"
        f"Actual safety flags: {route_fields['safety_flags']}"
    )

    assert route_fields["primary_condition"] == test_case["expected_primary_condition"], (
        f"Multi-label field test #{test_index} failed\n"
        f"Name: {test_case['name']}\n"
        f"Expected primary condition: {test_case['expected_primary_condition']}\n"
        f"Actual primary condition: {route_fields['primary_condition']}"
    )

    assert route_fields["primary_route"] == test_case["expected_primary_route"], (
        f"Multi-label field test #{test_index} failed\n"
        f"Name: {test_case['name']}\n"
        f"Expected primary route: {test_case['expected_primary_route']}\n"
        f"Actual primary route: {route_fields['primary_route']}"
    )

    assert route_fields["needs_clarification"] == test_case["expected_needs_clarification"], (
        f"Multi-label field test #{test_index} failed\n"
        f"Name: {test_case['name']}\n"
        f"Expected clarification: {test_case['expected_needs_clarification']}\n"
        f"Actual clarification: {route_fields['needs_clarification']}"
    )


total_tests = len(route_decision_test_cases) + len(multilabel_field_test_cases)

print(f"HYBRID ROUTE POLICY TEST: PASS ({total_tests}/{total_tests})")