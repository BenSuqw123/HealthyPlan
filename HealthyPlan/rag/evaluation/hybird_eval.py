from pathlib import Path

import pandas as pd

from config import Path_Root
from hybrid_condition_router import route_condition_hybrid


RAG_EVAL_DATA_PATH = f"{Path_Root}/data/rag/rag_eval_set.csv"

REQUIRED_COLUMNS = ["query", "condition_code"]

MIN_PRIMARY_OVERALL_ACCURACY = 0.90
MIN_PRIMARY_CONDITION_ACCURACY = 0.80
MIN_MULTILABEL_OVERALL_COVERAGE = 0.95
MIN_MULTILABEL_CONDITION_COVERAGE = 0.80


def load_evaluation_dataset():
    data_path = Path(RAG_EVAL_DATA_PATH)

    if not data_path.exists():
        raise FileNotFoundError(f"RAG evaluation dataset not found: {data_path}")

    dataframe = pd.read_csv(data_path, encoding="utf-8-sig")

    if dataframe.empty:
        raise ValueError("RAG evaluation dataset is empty.")

    dataframe.columns = dataframe.columns.str.strip()

    missing_columns = [column_name for column_name in REQUIRED_COLUMNS if column_name not in dataframe.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    evaluation_dataframe = dataframe.copy()
    evaluation_dataframe["query"] = evaluation_dataframe["query"].fillna("").astype(str).str.strip()
    evaluation_dataframe["condition_code"] = evaluation_dataframe["condition_code"].fillna("").astype(str).str.strip().str.lower()

    missing_value_rows = evaluation_dataframe[REQUIRED_COLUMNS].eq("").any(axis=1)

    if missing_value_rows.any():
        invalid_rows = evaluation_dataframe.loc[missing_value_rows, REQUIRED_COLUMNS]
        raise ValueError(f"Rows with missing required values:\n{invalid_rows.to_string(index=False)}")

    duplicated_queries = evaluation_dataframe["query"].str.lower().duplicated(keep=False)

    if duplicated_queries.any():
        duplicated_rows = evaluation_dataframe.loc[duplicated_queries, REQUIRED_COLUMNS]
        raise ValueError(f"Duplicate evaluation queries found:\n{duplicated_rows.to_string(index=False)}")

    return evaluation_dataframe.reset_index(drop=True)


def normalize_router_conditions(router_result):
    conditions = router_result.get("conditions", [])

    if not isinstance(conditions, list):
        return []

    normalized_conditions = []

    for condition_code in conditions:
        normalized_condition_code = str(condition_code or "").strip().lower()

        if normalized_condition_code and normalized_condition_code not in normalized_conditions:
            normalized_conditions.append(normalized_condition_code)

    return normalized_conditions


def calculate_multilabel_coverage(expected_condition, status, detected_condition, conditions):
    if status == "detected" and detected_condition == expected_condition:
        return True

    return expected_condition in conditions


def print_failed_result(index, evaluation_result, router_result):
    print(f"PRIMARY FAIL #{index + 1}")
    print(f"Query: {evaluation_result['query']}")
    print(f"Expected primary: {evaluation_result['expected_condition']}")
    print(f"Status: {evaluation_result['status']}")
    print(f"Detected primary: {evaluation_result['detected_condition']}")
    print(f"Extracted conditions: {evaluation_result['conditions']}")
    print(f"Safety flags: {evaluation_result['safety_flags']}")
    print(f"Primary correct: {evaluation_result['primary_is_correct']}")
    print(f"Multi-label covered: {evaluation_result['multilabel_is_correct']}")
    print(f"Decision reason: {evaluation_result['decision_reason']}")
    print(f"Top candidate: {evaluation_result['top_candidate']}")
    print(f"Best dense similarity: {evaluation_result['score']:.4f}")
    print(f"Fusion score: {evaluation_result['fusion_score']:.6f}")
    print(f"Score gap: {evaluation_result['score_gap']:.4f}")
    print("Hybrid results:")

    for hybrid_result in router_result["hybrid_results"]:
        hybrid_rank = hybrid_result["hybrid_rank"]
        condition_code = hybrid_result["condition_code"]
        dense_rank = hybrid_result["dense_rank"]
        bm25_rank = hybrid_result["bm25_rank"]
        rrf_score = hybrid_result["rrf_score"]
        matched_query = hybrid_result["query"]

        print(f"  {hybrid_rank}. [{condition_code}] dense={dense_rank} bm25={bm25_rank} rrf={rrf_score:.6f}")
        print(f"     {matched_query}")

    print("-" * 100)


def build_condition_summary(results_dataframe):
    condition_summary = results_dataframe.groupby("expected_condition").agg(
        total=("primary_is_correct", "size"),
        primary_correct=("primary_is_correct", "sum"),
        multilabel_covered=("multilabel_is_correct", "sum"),
    )

    condition_summary["primary_incorrect"] = condition_summary["total"] - condition_summary["primary_correct"]
    condition_summary["multilabel_missed"] = condition_summary["total"] - condition_summary["multilabel_covered"]
    condition_summary["primary_accuracy"] = condition_summary["primary_correct"] / condition_summary["total"]
    condition_summary["multilabel_coverage"] = condition_summary["multilabel_covered"] / condition_summary["total"]

    return condition_summary[
        [
            "total",
            "primary_correct",
            "primary_incorrect",
            "primary_accuracy",
            "multilabel_covered",
            "multilabel_missed",
            "multilabel_coverage",
        ]
    ]


def evaluate_hybrid_router():
    evaluation_dataframe = load_evaluation_dataset()
    evaluation_results = []

    print(f"Evaluation dataset: {RAG_EVAL_DATA_PATH}")
    print(f"Total evaluation queries: {len(evaluation_dataframe)}")
    print(f"Conditions: {evaluation_dataframe['condition_code'].nunique()}")
    print("=" * 100)

    for index in evaluation_dataframe.index:
        query = evaluation_dataframe.at[index, "query"]
        expected_condition = evaluation_dataframe.at[index, "condition_code"]

        router_result = route_condition_hybrid(query)

        status = router_result["status"]
        detected_condition = router_result["condition_code"]
        conditions = normalize_router_conditions(router_result)
        safety_flags = list(router_result.get("safety_flags", []))
        decision_reason = router_result.get("decision_reason", "unknown")
        score = float(router_result["score"])
        fusion_score = float(router_result["fusion_score"])
        score_gap = float(router_result["score_gap"])
        top_candidate = router_result["candidates"][0]["condition_code"] if router_result["candidates"] else None

        primary_is_correct = status == "detected" and detected_condition == expected_condition
        multilabel_is_correct = calculate_multilabel_coverage(expected_condition, status, detected_condition, conditions)

        evaluation_result = {
            "query": query,
            "expected_condition": expected_condition,
            "status": status,
            "detected_condition": detected_condition,
            "conditions": conditions,
            "safety_flags": safety_flags,
            "decision_reason": decision_reason,
            "top_candidate": top_candidate,
            "score": score,
            "fusion_score": fusion_score,
            "score_gap": score_gap,
            "primary_is_correct": primary_is_correct,
            "multilabel_is_correct": multilabel_is_correct,
        }

        evaluation_results.append(evaluation_result)

        if not primary_is_correct:
            print_failed_result(index, evaluation_result, router_result)

    results_dataframe = pd.DataFrame(evaluation_results)

    total_queries = len(results_dataframe)
    primary_correct_count = int(results_dataframe["primary_is_correct"].sum())
    primary_incorrect_count = total_queries - primary_correct_count
    multilabel_correct_count = int(results_dataframe["multilabel_is_correct"].sum())
    multilabel_incorrect_count = total_queries - multilabel_correct_count

    detected_count = int((results_dataframe["status"] == "detected").sum())
    ambiguous_count = int((results_dataframe["status"] == "ambiguous").sum())
    unknown_count = int((results_dataframe["status"] == "unknown").sum())

    primary_overall_accuracy = primary_correct_count / total_queries
    multilabel_overall_coverage = multilabel_correct_count / total_queries

    condition_summary = build_condition_summary(results_dataframe)
    lowest_primary_condition_accuracy = float(condition_summary["primary_accuracy"].min())
    lowest_multilabel_condition_coverage = float(condition_summary["multilabel_coverage"].min())

    predicted_labels = results_dataframe["detected_condition"].fillna(results_dataframe["status"])
    confusion_matrix = pd.crosstab(results_dataframe["expected_condition"], predicted_labels, rownames=["Expected"], colnames=["Predicted"])

    print("\n" + "=" * 100)
    print("HYBRID CONDITION ROUTER EVALUATION SUMMARY")
    print(f"Total queries: {total_queries}")
    print(f"Detected: {detected_count}")
    print(f"Ambiguous: {ambiguous_count}")
    print(f"Unknown: {unknown_count}")

    print("\nPrimary route evaluation:")
    print(f"Primary correct: {primary_correct_count}")
    print(f"Primary incorrect: {primary_incorrect_count}")
    print(f"Primary overall accuracy: {primary_overall_accuracy:.4f}")
    print(f"Minimum primary condition accuracy: {lowest_primary_condition_accuracy:.4f}")

    print("\nMulti-label evaluation:")
    print(f"Expected condition covered: {multilabel_correct_count}")
    print(f"Expected condition missed: {multilabel_incorrect_count}")
    print(f"Multi-label overall coverage: {multilabel_overall_coverage:.4f}")
    print(f"Minimum multi-label condition coverage: {lowest_multilabel_condition_coverage:.4f}")

    print("\nResults by condition:")
    print(condition_summary.to_string())

    print("\nPrimary confusion matrix:")
    print(confusion_matrix.to_string())

    primary_overall_passed = primary_overall_accuracy >= MIN_PRIMARY_OVERALL_ACCURACY
    primary_condition_passed = lowest_primary_condition_accuracy >= MIN_PRIMARY_CONDITION_ACCURACY
    multilabel_overall_passed = multilabel_overall_coverage >= MIN_MULTILABEL_OVERALL_COVERAGE
    multilabel_condition_passed = lowest_multilabel_condition_coverage >= MIN_MULTILABEL_CONDITION_COVERAGE

    if primary_overall_passed and primary_condition_passed and multilabel_overall_passed and multilabel_condition_passed:
        print("\nValidation: PASS")
    else:
        print("\nValidation: FAIL")

        if not primary_overall_passed:
            print(f"Primary overall accuracy must be at least {MIN_PRIMARY_OVERALL_ACCURACY:.2f}.")

        if not primary_condition_passed:
            print(f"Every primary condition accuracy must be at least {MIN_PRIMARY_CONDITION_ACCURACY:.2f}.")

        if not multilabel_overall_passed:
            print(f"Multi-label overall coverage must be at least {MIN_MULTILABEL_OVERALL_COVERAGE:.2f}.")

        if not multilabel_condition_passed:
            print(f"Every multi-label condition coverage must be at least {MIN_MULTILABEL_CONDITION_COVERAGE:.2f}.")

    print("=" * 100)


if __name__ == "__main__":
    evaluate_hybrid_router()