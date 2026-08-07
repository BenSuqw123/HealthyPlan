import re

from .entity_extractor import extract_medical_entities, find_first_pattern_match, normalize_entity_query


SUPPORTED_SAFETY_FLAGS = {
    "pregnancy",
    "elderly_frailty",
    "multiple_conditions",
    "conflicting_diet_rules",
    "inconsistent_lab_results",
    "medication_risk",
    "malnutrition_risk",
    "possible_emergency",
}


PREGNANCY_PATTERNS = [
    r"\bba bau\b",
    r"\bmang thai\b",
    r"\bthai phu\b",
    r"\bthai ky\b",
    r"\bpregnan(?:t|cy)\b",
]


ELDERLY_PATTERNS = [
    r"\bnguoi cao tuoi\b",
    r"\bnguoi gia\b",
    r"\blon tuoi\b",
    r"\belderly\b",
]


FRAILTY_PATTERNS = [
    r"\bteo co\b",
    r"\bmat co\b",
    r"\bsuy yeu\b",
    r"\bsuy nhuoc\b",
    r"\bsuy kiet\b",
    r"\bsarcopenia\b",
]


DIET_CONTEXT_PATTERNS = [
    r"\bche do an\b",
    r"\ban kieng\b",
    r"\bkieng an\b",
    r"\bdinh duong\b",
    r"\bthuc don\b",
    r"\bluong dam\b",
    r"\bluong kali\b",
    r"\bluong natri\b",
]


DIET_CONFLICT_PATTERNS = [
    r"\bmau thuan\b",
    r"\bxung dot\b",
    r"\buu tien (?:cai nao|the nao|quy tac nao)\b",
    r"\ban nhieu dam hay kieng dam\b",
    r"\bnen an .+ hay kieng .+\b",
    r"\bkieng .+ hay an .+\b",
]


LAB_TEST_PATTERNS = [
    r"\bcreatinine\b",
    r"\begfr\b",
    r"\bmuc loc cau than\b",
    r"\bchi so xet nghiem\b",
    r"\bket qua xet nghiem\b",
    r"\bduong huyet\b",
    r"\bkali mau\b",
    r"\bnatri mau\b",
]


INCONSISTENCY_PATTERNS = [
    r"\bkhong thong nhat\b",
    r"\bkhong khop\b",
    r"\bmau thuan\b",
    r"\bchenh lech\b",
    r"\btrai nguoc\b",
    r"\bkhong phu hop\b",
]


MEDICATION_PATTERNS = [
    r"\bthuoc\b",
    r"\blieu thuoc\b",
    r"\blieu luong\b",
    r"\binsulin\b",
    r"\bmetformin\b",
    r"\bthuoc huyet ap\b",
    r"\bthuoc tieu duong\b",
]


SELF_MEDICATION_ACTION_PATTERNS = [
    r"\btu y\b",
    r"\btu tang lieu\b",
    r"\btu giam lieu\b",
    r"\btu doi lieu\b",
    r"\btu doi thuoc\b",
    r"\btu ngung thuoc\b",
    r"\btu bo thuoc\b",
    r"\bco duoc tang lieu\b",
    r"\bco duoc giam lieu\b",
    r"\bco duoc doi thuoc\b",
    r"\bco duoc ngung thuoc\b",
    r"\buong them thuoc\b",
]


CLINICIAN_DIRECTION_PATTERNS = [
    r"\bbac si yeu cau\b",
    r"\bbac si chi dinh\b",
    r"\bbac si khuyen\b",
    r"\bbac si dieu chinh\b",
    r"\bduoc bac si yeu cau\b",
    r"\bduoc bac si chi dinh\b",
    r"\btheo chi dinh cua bac si\b",
    r"\btheo huong dan cua bac si\b",
    r"\bnhan vien y te yeu cau\b",
]


MALNUTRITION_PATTERNS = [
    r"\bsuy dinh duong\b",
    r"\bteo co\b",
    r"\bmat co\b",
    r"\bsuy kiet\b",
    r"\bthieu chat\b",
    r"\bsut can qua muc\b",
    r"\bgiam can qua muc\b",
    r"\bkieng khem qua muc\b",
]


EMERGENCY_PATTERNS = [
    r"\bcap cuu\b",
    r"\bkho tho\b",
    r"\bdau nguc\b",
    r"\bhon me\b",
    r"\bngat xiu\b",
    r"\bco giat\b",
    r"\bnhiem toan ceton\b",
    r"\bha duong huyet nghiem trong\b",
    r"\bchay mau khong cam\b",
]


def contains_safety_pattern(normalized_query, patterns):
    return find_first_pattern_match(normalized_query, patterns) is not None


def add_safety_flag(safety_flags, flag_matches, flag_code, matched_text, match_type):
    if flag_code not in SUPPORTED_SAFETY_FLAGS:
        raise ValueError(f"Unsupported safety flag: {flag_code}")

    if flag_code in safety_flags:
        return

    safety_flags.append(flag_code)

    flag_matches.append(
        {
            "flag_code": flag_code,
            "matched_text": matched_text,
            "match_type": match_type,
        }
    )


def extract_safety_flags(query, condition_codes=None):
    normalized_query = normalize_entity_query(query)

    if condition_codes is None:
        entity_result = extract_medical_entities(query)
        condition_codes = entity_result["condition_codes"]

    condition_codes = list(dict.fromkeys(condition_codes))
    safety_flags = []
    flag_matches = []

    pregnancy_match = find_first_pattern_match(normalized_query, PREGNANCY_PATTERNS)

    if pregnancy_match is not None:
        add_safety_flag(
            safety_flags,
            flag_matches,
            "pregnancy",
            pregnancy_match.group(0),
            "pregnancy_pattern",
        )

    elderly_match = find_first_pattern_match(normalized_query, ELDERLY_PATTERNS)
    frailty_match = find_first_pattern_match(normalized_query, FRAILTY_PATTERNS)

    if elderly_match is not None and frailty_match is not None:
        matched_text = f"{elderly_match.group(0)} | {frailty_match.group(0)}"

        add_safety_flag(
            safety_flags,
            flag_matches,
            "elderly_frailty",
            matched_text,
            "elderly_and_frailty_patterns",
        )

    if len(condition_codes) > 1:
        add_safety_flag(
            safety_flags,
            flag_matches,
            "multiple_conditions",
            " | ".join(condition_codes),
            "multiple_extracted_conditions",
        )

    diet_conflict_match = find_first_pattern_match(normalized_query, DIET_CONFLICT_PATTERNS)
    has_diet_context = contains_safety_pattern(normalized_query, DIET_CONTEXT_PATTERNS)

    if diet_conflict_match is not None:
        add_safety_flag(
            safety_flags,
            flag_matches,
            "conflicting_diet_rules",
            diet_conflict_match.group(0),
            "explicit_diet_conflict_pattern",
        )

    elif len(condition_codes) > 1 and has_diet_context and re.search(r"\bhay\b", normalized_query):
        add_safety_flag(
            safety_flags,
            flag_matches,
            "conflicting_diet_rules",
            "multiple conditions with alternative diet choices",
            "derived_diet_conflict",
        )

    lab_test_match = find_first_pattern_match(normalized_query, LAB_TEST_PATTERNS)
    inconsistency_match = find_first_pattern_match(normalized_query, INCONSISTENCY_PATTERNS)

    if lab_test_match is not None and inconsistency_match is not None:
        matched_text = f"{lab_test_match.group(0)} | {inconsistency_match.group(0)}"

        add_safety_flag(
            safety_flags,
            flag_matches,
            "inconsistent_lab_results",
            matched_text,
            "lab_test_and_inconsistency_patterns",
        )

    medication_match = find_first_pattern_match(normalized_query, MEDICATION_PATTERNS)
    self_medication_match = find_first_pattern_match(normalized_query, SELF_MEDICATION_ACTION_PATTERNS)
    clinician_direction_match = find_first_pattern_match(normalized_query, CLINICIAN_DIRECTION_PATTERNS)

    if medication_match is not None and self_medication_match is not None and clinician_direction_match is None:
        matched_text = f"{medication_match.group(0)} | {self_medication_match.group(0)}"

        add_safety_flag(
            safety_flags,
            flag_matches,
            "medication_risk",
            matched_text,
            "self_medication_pattern",
        )

    malnutrition_match = find_first_pattern_match(normalized_query, MALNUTRITION_PATTERNS)

    if malnutrition_match is not None:
        add_safety_flag(
            safety_flags,
            flag_matches,
            "malnutrition_risk",
            malnutrition_match.group(0),
            "malnutrition_pattern",
        )

    emergency_match = find_first_pattern_match(normalized_query, EMERGENCY_PATTERNS)

    if emergency_match is not None:
        add_safety_flag(
            safety_flags,
            flag_matches,
            "possible_emergency",
            emergency_match.group(0),
            "emergency_pattern",
        )

    return {
        "query": query,
        "normalized_query": normalized_query,
        "condition_codes": condition_codes,
        "safety_flags": safety_flags,
        "matches": flag_matches,
        "flag_count": len(safety_flags),
        "has_safety_flags": len(safety_flags) > 0,
    }