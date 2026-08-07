from .bm25_router import search_bm25_router
from .condition_router import search_router_examples
from .config import HYBRID_DENSE_TOP_N, HYBRID_BM25_TOP_N, HYBRID_FINAL_TOP_N, HYBRID_MATCH_WEIGHTS, HYBRID_CONSENSUS_MIN_SIMILARITY, HYBRID_CONSENSUS_MAX_BM25_RANK, RRF_K, ROUTER_MIN_SIMILARITY, ROUTER_MIN_SCORE_GAP, ROUTER_MAX_MATCHES_PER_CONDITION
from .entity_extractor import extract_medical_entities
from .safety_flag_extractor import extract_safety_flags


SAFETY_ROUTE_FLAGS = {
    "pregnancy",
    "elderly_frailty",
    "conflicting_diet_rules",
    "inconsistent_lab_results",
    "medication_risk",
    "malnutrition_risk",
    "possible_emergency",
}

def validate_positive_integer(value, parameter_name):
    if not isinstance(value, int):
        raise ValueError(f"{parameter_name} must be an integer.")

    if value <= 0:
        raise ValueError(f"{parameter_name} must be greater than zero.")


def validate_probability(value, parameter_name):
    if not isinstance(value, (int, float)):
        raise ValueError(f"{parameter_name} must be a number.")

    if value < 0 or value > 1:
        raise ValueError(f"{parameter_name} must be between zero and one.")


def validate_hybrid_config():
    if not isinstance(RRF_K, (int, float)):
        raise ValueError("RRF_K must be a number.")

    if RRF_K < 0:
        raise ValueError("RRF_K must be greater than or equal to zero.")

    validate_positive_integer(HYBRID_DENSE_TOP_N, "HYBRID_DENSE_TOP_N")
    validate_positive_integer(HYBRID_BM25_TOP_N, "HYBRID_BM25_TOP_N")
    validate_positive_integer(HYBRID_FINAL_TOP_N, "HYBRID_FINAL_TOP_N")
    validate_positive_integer(ROUTER_MAX_MATCHES_PER_CONDITION, "ROUTER_MAX_MATCHES_PER_CONDITION")
    validate_positive_integer(HYBRID_CONSENSUS_MAX_BM25_RANK, "HYBRID_CONSENSUS_MAX_BM25_RANK")

    validate_probability(HYBRID_CONSENSUS_MIN_SIMILARITY, "HYBRID_CONSENSUS_MIN_SIMILARITY")

    if not isinstance(HYBRID_MATCH_WEIGHTS, (list, tuple)):
        raise ValueError("HYBRID_MATCH_WEIGHTS must be a list or tuple.")

    if not HYBRID_MATCH_WEIGHTS:
        raise ValueError("HYBRID_MATCH_WEIGHTS cannot be empty.")

    for weight in HYBRID_MATCH_WEIGHTS:
        if not isinstance(weight, (int, float)):
            raise ValueError("Every hybrid match weight must be a number.")

        if weight <= 0:
            raise ValueError("Every hybrid match weight must be greater than zero.")


def calculate_rrf_score(rank):
    validate_positive_integer(rank, "rank")

    return float(1 / (RRF_K + rank))


def create_fused_result(result):
    fused_result = {
        "example_id": result.get("example_id"),
        "query": result.get("query"),
        "condition_code": result.get("condition_code"),
        "language": result.get("language"),
        "example_type": result.get("example_type"),
        "source_chunk_ids": result.get("source_chunk_ids"),
        "review_status": result.get("review_status"),
        "dense_rank": None,
        "dense_similarity": None,
        "bm25_rank": None,
        "bm25_score": None,
        "rrf_score": 0.0,
    }

    return fused_result


def validate_matching_example(fused_result, new_result):
    current_condition_code = str(fused_result.get("condition_code") or "").strip().lower()
    new_condition_code = str(new_result.get("condition_code") or "").strip().lower()

    if current_condition_code and new_condition_code and current_condition_code != new_condition_code:
        example_id = fused_result.get("example_id")
        raise ValueError(f"Condition mismatch for router example {example_id}: {current_condition_code} != {new_condition_code}")


def fuse_router_results(dense_results, bm25_results, final_top_n=HYBRID_FINAL_TOP_N):
    if not isinstance(dense_results, list):
        raise ValueError("dense_results must be a list.")

    if not isinstance(bm25_results, list):
        raise ValueError("bm25_results must be a list.")

    validate_positive_integer(final_top_n, "final_top_n")

    fused_results_by_id = {}

    for dense_rank, dense_result in enumerate(dense_results, start=1):
        example_id = dense_result.get("example_id")

        if not example_id:
            raise ValueError("Dense router result is missing example_id.")

        example_id = str(example_id)

        if example_id not in fused_results_by_id:
            fused_results_by_id[example_id] = create_fused_result(dense_result)
        else:
            validate_matching_example(fused_results_by_id[example_id], dense_result)

        fused_result = fused_results_by_id[example_id]
        fused_result["dense_rank"] = dense_rank
        fused_result["dense_similarity"] = float(dense_result.get("similarity", 0.0))
        fused_result["rrf_score"] += calculate_rrf_score(dense_rank)

    for bm25_rank, bm25_result in enumerate(bm25_results, start=1):
        example_id = bm25_result.get("example_id")

        if not example_id:
            raise ValueError("BM25 router result is missing example_id.")

        example_id = str(example_id)

        if example_id not in fused_results_by_id:
            fused_results_by_id[example_id] = create_fused_result(bm25_result)
        else:
            validate_matching_example(fused_results_by_id[example_id], bm25_result)

        fused_result = fused_results_by_id[example_id]
        fused_result["bm25_rank"] = bm25_rank
        fused_result["bm25_score"] = float(bm25_result.get("bm25_score", 0.0))
        fused_result["rrf_score"] += calculate_rrf_score(bm25_rank)

    fused_results = list(fused_results_by_id.values())

    for fused_result in fused_results:
        fused_result["example_id"] = str(fused_result.get("example_id") or "")
        fused_result["condition_code"] = str(fused_result.get("condition_code") or "").strip().lower()
        fused_result["query"] = str(fused_result.get("query") or "")
        fused_result["rrf_score"] = float(fused_result["rrf_score"])

        if not fused_result["condition_code"]:
            raise ValueError(f"Fused router result is missing condition_code: {fused_result['example_id']}")

    fused_results = sorted(
        fused_results,
        key=lambda item: (
            -item["rrf_score"],
            item["dense_rank"] if item["dense_rank"] is not None else 999999,
            item["bm25_rank"] if item["bm25_rank"] is not None else 999999,
            item["example_id"],
        ),
    )

    fused_results = fused_results[:final_top_n]

    for hybrid_rank, fused_result in enumerate(fused_results, start=1):
        fused_result["hybrid_rank"] = hybrid_rank

    return fused_results


def calculate_discounted_condition_score(selected_examples):
    if not selected_examples:
        return 0.0

    available_weight_count = min(len(selected_examples), len(HYBRID_MATCH_WEIGHTS))
    discounted_score = 0.0

    for index in range(available_weight_count):
        example = selected_examples[index]
        weight = float(HYBRID_MATCH_WEIGHTS[index])
        discounted_score += float(example["rrf_score"]) * weight

    return float(discounted_score)


def build_hybrid_condition_candidates(hybrid_results):
    if not isinstance(hybrid_results, list):
        raise ValueError("hybrid_results must be a list.")

    condition_groups = {}

    for hybrid_result in hybrid_results:
        condition_code = str(hybrid_result.get("condition_code") or "").strip().lower()

        if not condition_code:
            continue

        if condition_code not in condition_groups:
            condition_groups[condition_code] = []

        condition_groups[condition_code].append(hybrid_result)

    candidates = []

    for condition_code, matched_examples in condition_groups.items():
        matched_examples = sorted(
            matched_examples,
            key=lambda item: (
                item["hybrid_rank"],
                -item["rrf_score"],
                item["example_id"],
            ),
        )

        maximum_selected_matches = min(ROUTER_MAX_MATCHES_PER_CONDITION, len(HYBRID_MATCH_WEIGHTS))
        selected_examples = matched_examples[:maximum_selected_matches]
        fusion_score = calculate_discounted_condition_score(selected_examples)

        dense_similarities = [float(item["dense_similarity"]) for item in matched_examples if item["dense_similarity"] is not None]
        dense_ranks = [int(item["dense_rank"]) for item in matched_examples if item["dense_rank"] is not None]
        bm25_ranks = [int(item["bm25_rank"]) for item in matched_examples if item["bm25_rank"] is not None]

        best_dense_similarity = max(dense_similarities) if dense_similarities else 0.0
        best_dense_rank = min(dense_ranks) if dense_ranks else None
        best_bm25_rank = min(bm25_ranks) if bm25_ranks else None
        best_hybrid_rank = min(item["hybrid_rank"] for item in matched_examples)

        dense_match_count = len(dense_ranks)
        bm25_match_count = len(bm25_ranks)
        same_example_consensus_count = sum(1 for item in matched_examples if item["dense_rank"] is not None and item["bm25_rank"] is not None)

        has_dense_support = dense_match_count > 0
        has_bm25_support = bm25_match_count > 0
        has_cross_retriever_support = has_dense_support and has_bm25_support
        has_same_example_consensus = same_example_consensus_count > 0

        candidate = {
            "condition_code": condition_code,
            "fusion_score": float(fusion_score),
            "best_dense_similarity": float(best_dense_similarity),
            "best_dense_rank": best_dense_rank,
            "best_bm25_rank": best_bm25_rank,
            "best_hybrid_rank": int(best_hybrid_rank),
            "match_count": len(matched_examples),
            "selected_match_count": len(selected_examples),
            "dense_match_count": dense_match_count,
            "bm25_match_count": bm25_match_count,
            "same_example_consensus_count": same_example_consensus_count,
            "has_dense_support": has_dense_support,
            "has_bm25_support": has_bm25_support,
            "has_cross_retriever_support": has_cross_retriever_support,
            "has_same_example_consensus": has_same_example_consensus,
            "selected_examples": selected_examples,
            "matched_examples": matched_examples,
        }

        candidates.append(candidate)

    candidates = sorted(
        candidates,
        key=lambda item: (
            -item["fusion_score"],
            -int(item["has_same_example_consensus"]),
            -int(item["has_cross_retriever_support"]),
            -item["best_dense_similarity"],
            item["best_hybrid_rank"],
            item["condition_code"],
        ),
    )

    return candidates


def search_hybrid_router(query, dense_top_n=HYBRID_DENSE_TOP_N, bm25_top_n=HYBRID_BM25_TOP_N, final_top_n=HYBRID_FINAL_TOP_N):
    validate_hybrid_config()
    validate_positive_integer(dense_top_n, "dense_top_n")
    validate_positive_integer(bm25_top_n, "bm25_top_n")
    validate_positive_integer(final_top_n, "final_top_n")

    dense_search_result = search_router_examples(query, top_n=dense_top_n)
    bm25_search_result = search_bm25_router(query, top_n=bm25_top_n)

    dense_results = dense_search_result.get("router_results", [])
    bm25_results = bm25_search_result.get("bm25_results", [])

    hybrid_results = fuse_router_results(dense_results, bm25_results, final_top_n=final_top_n)
    candidates = build_hybrid_condition_candidates(hybrid_results)

    search_result = {
        "processed_query": dense_search_result["processed_query"],
        "dense_results": dense_results,
        "bm25_results": bm25_results,
        "hybrid_results": hybrid_results,
        "candidates": candidates,
    }

    return search_result


def calculate_relative_score_gap(best_score, second_score):
    best_score = float(best_score)
    second_score = float(second_score)

    if best_score <= 0:
        return 0.0

    raw_score_gap = best_score - second_score
    relative_score_gap = raw_score_gap / best_score

    return float(relative_score_gap)


def has_hybrid_consensus(candidate):
    if not candidate["has_cross_retriever_support"]:
        return False

    if candidate["best_dense_similarity"] < HYBRID_CONSENSUS_MIN_SIMILARITY:
        return False

    if candidate["best_bm25_rank"] is None:
        return False

    if candidate["best_bm25_rank"] > HYBRID_CONSENSUS_MAX_BM25_RANK:
        return False

    return True

def has_safety_route_override(safety_flags):
    for safety_flag in safety_flags:
        if safety_flag in SAFETY_ROUTE_FLAGS:
            return True

    return False


def resolve_route_decision(status, condition_code, entity_result, safety_result):
    condition_codes = entity_result["condition_codes"]
    safety_flags = safety_result["safety_flags"]

    if has_safety_route_override(safety_flags):
        return {
            "status": "detected",
            "condition_code": "general_safety",
            "decision_reason": "safety_flag_override",
        }

    if len(condition_codes) == 1:
        return {
            "status": "detected",
            "condition_code": condition_codes[0],
            "decision_reason": "explicit_entity_override",
        }

    return {
        "status": status,
        "condition_code": condition_code,
        "decision_reason": "hybrid_router",
    }


def build_multilabel_route_fields(status, condition_code, entity_result, safety_result):
    conditions = list(entity_result["condition_codes"])
    safety_flags = list(safety_result["safety_flags"])

    primary_condition = None
    primary_route = "unknown"
    needs_clarification = False

    if status == "detected":
        if condition_code == "general_safety":
            primary_route = "general_safety"
        else:
            primary_condition = condition_code
            primary_route = "condition"

            if condition_code and condition_code not in conditions:
                conditions.insert(0, condition_code)

    elif status == "ambiguous":
        primary_route = "clarification"
        needs_clarification = True

    elif status == "unknown":
        primary_route = "unknown"
        needs_clarification = True

    return {
        "conditions": conditions,
        "safety_flags": safety_flags,
        "primary_condition": primary_condition,
        "primary_route": primary_route,
        "needs_clarification": needs_clarification,
        "entity_matches": entity_result["matches"],
        "safety_flag_matches": safety_result["matches"],
    }


def build_route_result(processed_query, status, condition_code, best_candidate, candidates, hybrid_results, score_gap, min_similarity, entity_result, safety_result, decision_reason):
    if best_candidate is None:
        best_dense_similarity = 0.0
        fusion_score = 0.0
        dense_confident = False
        hybrid_consensus = False
    else:
        best_dense_similarity = float(best_candidate["best_dense_similarity"])
        fusion_score = float(best_candidate["fusion_score"])
        dense_confident = best_dense_similarity >= min_similarity
        hybrid_consensus = has_hybrid_consensus(best_candidate)

    multilabel_fields = build_multilabel_route_fields(status, condition_code, entity_result, safety_result)

    result = {
        "query": processed_query["normalized_query"],
        "status": status,
        "condition_code": condition_code,
        "conditions": multilabel_fields["conditions"],
        "safety_flags": multilabel_fields["safety_flags"],
        "primary_condition": multilabel_fields["primary_condition"],
        "primary_route": multilabel_fields["primary_route"],
        "needs_clarification": multilabel_fields["needs_clarification"],
        "entity_matches": multilabel_fields["entity_matches"],
        "safety_flag_matches": multilabel_fields["safety_flag_matches"],
        "score": float(best_dense_similarity),
        "fusion_score": float(fusion_score),
        "score_gap": float(score_gap),
        "dense_confident": dense_confident,
        "hybrid_consensus": hybrid_consensus,
        "decision_reason": decision_reason,
        "route_method": "hybrid_rrf_discounted_support_with_entity_and_safety_policy",
        "candidates": candidates,
        "hybrid_results": hybrid_results,
    }

    return result


def finalize_route_result(processed_query, status, condition_code, best_candidate, candidates, hybrid_results, score_gap, min_similarity, entity_result, safety_result):
    route_decision = resolve_route_decision(status, condition_code, entity_result, safety_result)

    return build_route_result(
        processed_query,
        route_decision["status"],
        route_decision["condition_code"],
        best_candidate,
        candidates,
        hybrid_results,
        score_gap,
        min_similarity,
        entity_result,
        safety_result,
        route_decision["decision_reason"],
    )


def route_condition_hybrid(query, dense_top_n=HYBRID_DENSE_TOP_N, bm25_top_n=HYBRID_BM25_TOP_N, final_top_n=HYBRID_FINAL_TOP_N, min_similarity=ROUTER_MIN_SIMILARITY, min_score_gap=ROUTER_MIN_SCORE_GAP):
    validate_positive_integer(dense_top_n, "dense_top_n")
    validate_positive_integer(bm25_top_n, "bm25_top_n")
    validate_positive_integer(final_top_n, "final_top_n")
    validate_probability(min_similarity, "min_similarity")
    validate_probability(min_score_gap, "min_score_gap")

    entity_result = extract_medical_entities(query)
    safety_result = extract_safety_flags(query, entity_result["condition_codes"])
    search_result = search_hybrid_router(query, dense_top_n=dense_top_n, bm25_top_n=bm25_top_n, final_top_n=final_top_n)

    processed_query = search_result["processed_query"]
    candidates = search_result["candidates"]
    hybrid_results = search_result["hybrid_results"]

    if not candidates:
        return finalize_route_result(processed_query, "unknown", None, None, candidates, hybrid_results, 0.0, min_similarity, entity_result, safety_result)

    best_candidate = candidates[0]
    best_condition_code = best_candidate["condition_code"]
    best_fusion_score = float(best_candidate["fusion_score"])

    second_fusion_score = float(candidates[1]["fusion_score"]) if len(candidates) > 1 else 0.0
    relative_score_gap = calculate_relative_score_gap(best_fusion_score, second_fusion_score)

    dense_confident = best_candidate["best_dense_similarity"] >= min_similarity
    hybrid_consensus = has_hybrid_consensus(best_candidate)
    has_reliable_evidence = dense_confident or hybrid_consensus

    if not has_reliable_evidence:
        return finalize_route_result(processed_query, "unknown", None, best_candidate, candidates, hybrid_results, relative_score_gap, min_similarity, entity_result, safety_result)

    if len(candidates) > 1 and relative_score_gap < min_score_gap:
        return finalize_route_result(processed_query, "ambiguous", None, best_candidate, candidates, hybrid_results, relative_score_gap, min_similarity, entity_result, safety_result)

    return finalize_route_result(processed_query, "detected", best_condition_code, best_candidate, candidates, hybrid_results, relative_score_gap, min_similarity, entity_result, safety_result)