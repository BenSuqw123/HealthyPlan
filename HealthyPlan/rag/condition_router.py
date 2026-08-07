import re
from .config import ROUTER_TOP_N, ROUTER_MIN_SIMILARITY, ROUTER_MIN_SCORE_GAP, ROUTER_MAX_MATCHES_PER_CONDITION
from .query_processor import process_query
from .vector_store import embedding_texts, get_condition_router_collection


def calculate_rank_weight(rank, total_results):
    if total_results <= 0:
        return 0.0

    rank_weight = (total_results - rank + 1) / total_results

    return float(rank_weight)


def build_condition_candidates(router_results):
    condition_groups = {}

    total_results = len(router_results)

    for rank, result in enumerate(router_results, start=1):
        condition_code = result["condition_code"]
        rank_weight = calculate_rank_weight(rank, total_results)
        vote_contribution = result["similarity"] * rank_weight

        matched_example = {
            "rank": rank,
            "example_id": result["example_id"],
            "query": result["query"],
            "similarity": result["similarity"],
            "rank_weight": rank_weight,
            "vote_contribution": vote_contribution,
            "example_type": result["example_type"],
            "source_chunk_ids": result["source_chunk_ids"],
        }

        if condition_code not in condition_groups:
            condition_groups[condition_code] = {
                "matched_examples": [],
            }

        condition_groups[condition_code]["matched_examples"].append(matched_example)

    candidates = []

    for condition_code, condition_group in condition_groups.items():
        matched_examples = condition_group["matched_examples"]
        matched_examples = sorted(matched_examples, key=lambda item: item["rank"])

        selected_examples = matched_examples[:ROUTER_MAX_MATCHES_PER_CONDITION]

        similarities = []

        for matched_example in selected_examples:
            similarities.append(matched_example["similarity"])

        vote_score = 0.0

        for matched_example in selected_examples:
            vote_score += matched_example["vote_contribution"]

        best_similarity = max(similarities)
        average_similarity = sum(similarities) / len(similarities)

        candidate = {
            "condition_code": condition_code,
            "vote_score": float(vote_score),
            "best_similarity": float(best_similarity),
            "average_similarity": float(average_similarity),
            "match_count": len(matched_examples),
            "selected_match_count": len(selected_examples),
            "matched_examples": matched_examples,
        }

        candidates.append(candidate)

    candidates = sorted(candidates, key=lambda item: item["vote_score"], reverse=True)

    return candidates


def search_router_examples(query, top_n=ROUTER_TOP_N):
    processed_query = process_query(query)
    normalized_query = processed_query["normalized_query"]

    if not isinstance(top_n, int):
        raise ValueError("top_n must be an integer.")

    if top_n <= 0:
        raise ValueError("top_n must be greater than zero.")

    collection = get_condition_router_collection()
    collection_count = collection.count()

    if collection_count == 0:
        raise ValueError("Condition router collection is empty.")

    actual_top_n = min(top_n, collection_count)

    query_embeddings = embedding_texts(normalized_query)
    query_embedding = query_embeddings[0].tolist()

    query_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=actual_top_n,
        include=["documents", "metadatas", "distances"],
    )

    documents = query_results["documents"][0]
    metadatas = query_results["metadatas"][0]
    distances = query_results["distances"][0]

    router_results = []

    for index in range(len(documents)):
        document = documents[index]
        metadata = metadatas[index]
        distance = float(distances[index])
        similarity = float(1 - distance)

        router_result = {
            "rank": index + 1,
            "example_id": metadata.get("example_id"),
            "query": document,
            "condition_code": metadata.get("condition_code"),
            "example_type": metadata.get("example_type"),
            "source_chunk_ids": metadata.get("source_chunk_ids"),
            "distance": distance,
            "similarity": similarity,
        }

        router_results.append(router_result)

    search_result = {
        "processed_query": processed_query,
        "router_results": router_results,
    }

    return search_result


def route_condition(query, top_n=ROUTER_TOP_N, min_similarity=ROUTER_MIN_SIMILARITY, min_score_gap=ROUTER_MIN_SCORE_GAP):
    search_result = search_router_examples(query, top_n=top_n)

    processed_query = search_result["processed_query"]
    router_results = search_result["router_results"]
    candidates = build_condition_candidates(router_results)

    if not candidates:
        return {
            "query": processed_query["normalized_query"],
            "status": "unknown",
            "condition_code": None,
            "score": 0.0,
            "vote_score": 0.0,
            "score_gap": 0.0,
            "candidates": [],
            "router_results": router_results,
        }

    best_candidate = candidates[0]
    best_condition_code = best_candidate["condition_code"]
    best_similarity = best_candidate["best_similarity"]
    best_vote_score = best_candidate["vote_score"]

    second_vote_score = 0.0

    if len(candidates) > 1:
        second_vote_score = candidates[1]["vote_score"]

    raw_score_gap = best_vote_score - second_vote_score

    if best_vote_score > 0:
        relative_score_gap = raw_score_gap / best_vote_score
    else:
        relative_score_gap = 0.0

    if best_similarity < min_similarity:
        return {
            "query": processed_query["normalized_query"],
            "status": "unknown",
            "condition_code": None,
            "score": best_similarity,
            "vote_score": best_vote_score,
            "score_gap": relative_score_gap,
            "candidates": candidates,
            "router_results": router_results,
        }

    if len(candidates) > 1 and relative_score_gap < min_score_gap:
        return {
            "query": processed_query["normalized_query"],
            "status": "ambiguous",
            "condition_code": None,
            "score": best_similarity,
            "vote_score": best_vote_score,
            "score_gap": relative_score_gap,
            "candidates": candidates,
            "router_results": router_results,
        }

    return {
        "query": processed_query["normalized_query"],
        "status": "detected",
        "condition_code": best_condition_code,
        "score": best_similarity,
        "vote_score": best_vote_score,
        "score_gap": relative_score_gap,
        "candidates": candidates,
        "router_results": router_results,
    }