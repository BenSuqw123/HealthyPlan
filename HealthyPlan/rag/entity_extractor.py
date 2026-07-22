import re
import unicodedata


SUPPORTED_CONDITION_CODES = {
    "diabetes_type_1",
    "diabetes_type_2",
    "prediabetes",
    "hypertension",
    "gout",
    "obesity",
    "ckd_g1",
    "ckd_g2",
    "ckd_g3a",
    "ckd_g3b",
    "ckd_g4",
    "ckd_g5_non_dialysis",
    "ckd_dialysis",
}


CONDITION_PATTERNS = {
    "diabetes_type_1": [
        r"\b(?:tieu duong|dai thao duong|diabetes)\s*(?:type|tuyp|tip)\s*1\b",
        r"\b(?:type|tuyp|tip)\s*1\s*(?:diabetes|tieu duong|dai thao duong)\b",
        r"\bt1d\b",
    ],
    "diabetes_type_2": [
        r"\b(?:tieu duong|dai thao duong|diabetes)\s*(?:type|tuyp|tip)\s*2\b",
        r"\b(?:type|tuyp|tip)\s*2\s*(?:diabetes|tieu duong|dai thao duong)\b",
        r"\bt2d\b",
    ],
    "prediabetes": [
        r"\bpre[\s-]?diabetes\b",
        r"\btien tieu duong\b",
        r"\btien dai thao duong\b",
    ],
    "hypertension": [
        r"\btang huyet ap\b",
        r"\bcao huyet ap\b",
        r"\bhypertension\b",
    ],
    "gout": [
        r"\bgout\b",
        r"\bgut\b",
        r"\bthong phong\b",
    ],
    "obesity": [
        r"\bbeo phi\b",
        r"\bobesity\b",
    ],
}


CKD_STAGE_PATTERNS = {
    "ckd_g1": [
        r"\bckd\s*(?:stage\s*|giai doan\s*|do\s*)?g?1\b",
        r"\b(?:suy than|benh than man|than man)\s*(?:stage\s*|giai doan\s*|do\s*)?g?1\b",
    ],
    "ckd_g2": [
        r"\bckd\s*(?:stage\s*|giai doan\s*|do\s*)?g?2\b",
        r"\b(?:suy than|benh than man|than man)\s*(?:stage\s*|giai doan\s*|do\s*)?g?2\b",
    ],
    "ckd_g3a": [
        r"\bckd\s*(?:stage\s*|giai doan\s*|do\s*)?g?3a\b",
        r"\b(?:suy than|benh than man|than man)\s*(?:stage\s*|giai doan\s*|do\s*)?g?3a\b",
    ],
    "ckd_g3b": [
        r"\bckd\s*(?:stage\s*|giai doan\s*|do\s*)?g?3b\b",
        r"\b(?:suy than|benh than man|than man)\s*(?:stage\s*|giai doan\s*|do\s*)?g?3b\b",
    ],
    "ckd_g4": [
        r"\bckd\s*(?:stage\s*|giai doan\s*|do\s*)?g?4\b",
        r"\b(?:suy than|benh than man|than man)\s*(?:stage\s*|giai doan\s*|do\s*)?g?4\b",
    ],
    "ckd_g5_non_dialysis": [
        r"\bckd\s*(?:stage\s*|giai doan\s*|do\s*)?g?5\b",
        r"\b(?:suy than|benh than man|than man)\s*(?:stage\s*|giai doan\s*|do\s*)?g?5\b",
    ],
}


DIALYSIS_PATTERNS = [
    r"\bdang chay than\b",
    r"\bchay than nhan tao\b",
    r"\bdang loc mau\b",
    r"\btham tach mau\b",
    r"\bloc mang bung\b",
    r"\bdialysis\b",
    r"\bhemodialysis\b",
    r"\bperitoneal dialysis\b",
]


NON_DIALYSIS_PATTERNS = [
    r"\bchua chay than\b",
    r"\bchua loc mau\b",
    r"\bkhong chay than\b",
    r"\bkhong loc mau\b",
    r"\btruoc loc mau\b",
    r"\bnon[\s-]?dialysis\b",
]


PRE_DIALYSIS_PATTERNS = [
    r"\bchuan bi chay than\b",
    r"\bchuan bi chay than nhan tao\b",
    r"\bchuan bi loc mau\b",
    r"\bde chuan bi chay than\b",
    r"\bde chuan bi loc mau\b",
    r"\btruoc khi chay than\b",
    r"\btruoc khi loc mau\b",
    r"\bke hoach chay than\b",
    r"\bke hoach loc mau\b",
    r"\bdu kien chay than\b",
    r"\bdu kien loc mau\b",
    r"\bse chay than\b",
    r"\bse loc mau\b",
    r"\btao cau noi chay than\b",
    r"\blam cau noi chay than\b",
    r"\bbao ve tinh mach.+chay than\b",
]


def normalize_entity_query(query):
    if not isinstance(query, str):
        raise ValueError("query must be a string.")

    normalized_query = unicodedata.normalize("NFKC", query).lower().strip()
    normalized_query = normalized_query.replace("đ", "d")

    decomposed_query = unicodedata.normalize("NFD", normalized_query)
    normalized_query = "".join(
        character
        for character in decomposed_query
        if unicodedata.category(character) != "Mn"
    )

    normalized_query = re.sub(r"[^a-z0-9]+", " ", normalized_query)
    normalized_query = re.sub(r"\s+", " ", normalized_query).strip()

    return normalized_query


def find_first_pattern_match(query, patterns):
    first_match = None

    for pattern in patterns:
        current_match = re.search(pattern, query, flags=re.IGNORECASE)

        if current_match is None:
            continue

        if first_match is None or current_match.start() < first_match.start():
            first_match = current_match

    return first_match


def contains_pattern(query, patterns):
    return find_first_pattern_match(query, patterns) is not None


def create_entity_match(condition_code, pattern_match, match_type):
    if condition_code not in SUPPORTED_CONDITION_CODES:
        raise ValueError(f"Unsupported condition code: {condition_code}")

    return {
        "condition_code": condition_code,
        "matched_text": pattern_match.group(0),
        "start": int(pattern_match.start()),
        "end": int(pattern_match.end()),
        "match_type": match_type,
    }


def extract_general_condition_matches(normalized_query):
    entity_matches = []

    for condition_code, patterns in CONDITION_PATTERNS.items():
        pattern_match = find_first_pattern_match(normalized_query, patterns)

        if pattern_match is None:
            continue

        entity_match = create_entity_match(
            condition_code,
            pattern_match,
            "condition_pattern",
        )

        entity_matches.append(entity_match)

    return entity_matches


def extract_ckd_condition_matches(normalized_query):
    entity_matches = []

    has_dialysis = contains_pattern(
        normalized_query,
        DIALYSIS_PATTERNS,
    )

    has_non_dialysis = contains_pattern(
        normalized_query,
        NON_DIALYSIS_PATTERNS,
    )

    has_pre_dialysis = contains_pattern(
        normalized_query,
        PRE_DIALYSIS_PATTERNS,
    )

    is_currently_on_dialysis = (
        has_dialysis
        and not has_non_dialysis
        and not has_pre_dialysis
    )

    if is_currently_on_dialysis:
        dialysis_match = find_first_pattern_match(
            normalized_query,
            DIALYSIS_PATTERNS,
        )

        if dialysis_match is not None:
            entity_match = create_entity_match(
                "ckd_dialysis",
                dialysis_match,
                "dialysis_pattern",
            )

            entity_matches.append(entity_match)

        return entity_matches

    for condition_code, patterns in CKD_STAGE_PATTERNS.items():
        pattern_match = find_first_pattern_match(
            normalized_query,
            patterns,
        )

        if pattern_match is None:
            continue

        entity_match = create_entity_match(
            condition_code,
            pattern_match,
            "ckd_stage_pattern",
        )

        entity_matches.append(entity_match)

    return entity_matches


def get_unique_condition_codes(entity_matches):
    condition_codes = []

    for entity_match in entity_matches:
        condition_code = entity_match["condition_code"]

        if condition_code not in condition_codes:
            condition_codes.append(condition_code)

    return condition_codes


def extract_medical_entities(query):
    normalized_query = normalize_entity_query(query)

    general_condition_matches = extract_general_condition_matches(
        normalized_query,
    )

    ckd_condition_matches = extract_ckd_condition_matches(
        normalized_query,
    )

    entity_matches = (
        general_condition_matches
        + ckd_condition_matches
    )

    entity_matches = sorted(
        entity_matches,
        key=lambda item: (
            item["start"],
            item["end"],
            item["condition_code"],
        ),
    )

    condition_codes = get_unique_condition_codes(
        entity_matches,
    )

    return {
        "query": query,
        "normalized_query": normalized_query,
        "condition_codes": condition_codes,
        "matches": entity_matches,
        "condition_count": len(condition_codes),
        "has_multiple_conditions": len(condition_codes) > 1,
    }