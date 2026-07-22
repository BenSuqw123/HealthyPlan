from pathlib import Path

import pandas as pd

from config import Path_Root
from condition_router import route_condition


RAG_EVAL_DATA_PATH = f"{Path_Root}/data/rag/rag_eval_set.csv"

REQUIRED_COLUMNS = ["query", "condition_code"]

MIN_OVERALL_ACCURACY = 0.90
MIN_CONDITION_ACCURACY = 0.80


def load_evaluation_dataset():
    data_path = Path(RAG_EVAL_DATA_PATH)

    if not data_path.exists():
        raise FileNotFoundError(f"RAG evaluation dataset not found: {data_path}")

    dataframe = pd.read_csv(data_path, encoding="utf-8-sig")

    if dataframe.empty:
        raise ValueError("RAG evaluation dataset is empty.")

    dataframe.columns = dataframe.columns.str.strip()

    missing_columns = []

    for column_name in REQUIRED_COLUMNS:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

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

    evaluation_dataframe = evaluation_dataframe.reset_index(drop=True)

    return evaluation_dataframe


def evaluate_router():
    evaluation_dataframe = load_evaluation_dataset()

    evaluation_results = []

    print(f"Evaluation dataset: {RAG_EVAL_DATA_PATH}")
    print(f"Total evaluation queries: {len(evaluation_dataframe)}")
    print(f"Conditions: {evaluation_dataframe['condition_code'].nunique()}")
    print("=" * 90)

    for index in evaluation_dataframe.index:
        query = evaluation_dataframe.at[index, "query"]
        expected_condition = evaluation_dataframe.at[index, "condition_code"]

        router_result = route_condition(query)

        status = router_result["status"]
        detected_condition = router_result["condition_code"]
        score = float(router_result["score"])
        vote_score = float(router_result.get("vote_score", 0.0))
        score_gap = float(router_result["score_gap"])

        is_correct = status == "detected" and detected_condition == expected_condition

        top_candidate = None

        if router_result["candidates"]:
            top_candidate = router_result["candidates"][0]["condition_code"]

        evaluation_result = {
            "query": query,
            "expected_condition": expected_condition,
            "status": status,
            "detected_condition": detected_condition,
            "top_candidate": top_candidate,
            "score": score,
            "vote_score": vote_score,
            "score_gap": score_gap,
            "is_correct": is_correct,
        }

        evaluation_results.append(evaluation_result)

        if not is_correct:
            print(f"FAIL #{index + 1}")
            print(f"Query: {query}")
            print(f"Expected: {expected_condition}")
            print(f"Status: {status}")
            print(f"Detected: {detected_condition}")
            print(f"Top candidate: {top_candidate}")
            print(f"Similarity: {score:.4f}")
            print(f"Vote score: {vote_score:.4f}")
            print(f"Score gap: {score_gap:.4f}")

            print("Nearest examples:")

            for router_example in router_result["router_results"]:
                example_condition = router_example["condition_code"]
                example_similarity = router_example["similarity"]
                example_query = router_example["query"]

                print(f"  [{example_condition}] {example_similarity:.4f} - {example_query}")

            print("-" * 90)

    results_dataframe = pd.DataFrame(evaluation_results)

    total_queries = len(results_dataframe)
    correct_count = int(results_dataframe["is_correct"].sum())
    failed_count = total_queries - correct_count

    detected_count = int((results_dataframe["status"] == "detected").sum())
    ambiguous_count = int((results_dataframe["status"] == "ambiguous").sum())
    unknown_count = int((results_dataframe["status"] == "unknown").sum())

    overall_accuracy = correct_count / total_queries

    condition_summary = results_dataframe.groupby("expected_condition").agg(
        total=("is_correct", "size"),
        correct=("is_correct", "sum"),
    )

    condition_summary["incorrect"] = condition_summary["total"] - condition_summary["correct"]
    condition_summary["accuracy"] = condition_summary["correct"] / condition_summary["total"]

    lowest_condition_accuracy = float(condition_summary["accuracy"].min())

    print("\n" + "=" * 90)
    print("CONDITION ROUTER EVALUATION SUMMARY")
    print(f"Total queries: {total_queries}")
    print(f"Correct: {correct_count}")
    print(f"Incorrect: {failed_count}")
    print(f"Detected: {detected_count}")
    print(f"Ambiguous: {ambiguous_count}")
    print(f"Unknown: {unknown_count}")
    print(f"Overall accuracy: {overall_accuracy:.4f}")
    print(f"Minimum condition accuracy: {lowest_condition_accuracy:.4f}")

    print("\nResults by condition:")
    print(condition_summary.to_string())

    predicted_labels = results_dataframe["detected_condition"].fillna(results_dataframe["status"])
    confusion_matrix = pd.crosstab(results_dataframe["expected_condition"], predicted_labels, rownames=["Expected"], colnames=["Predicted"])

    print("\nConfusion matrix:")
    print(confusion_matrix.to_string())

    overall_accuracy_passed = overall_accuracy >= MIN_OVERALL_ACCURACY
    condition_accuracy_passed = lowest_condition_accuracy >= MIN_CONDITION_ACCURACY

    if overall_accuracy_passed and condition_accuracy_passed:
        print("\nValidation: PASS")
    else:
        print("\nValidation: FAIL")

        if not overall_accuracy_passed:
            print(f"Overall accuracy must be at least {MIN_OVERALL_ACCURACY:.2f}.")

        if not condition_accuracy_passed:
            print(f"Every condition accuracy must be at least {MIN_CONDITION_ACCURACY:.2f}.")

    print("=" * 90)


if __name__ == "__main__":
    evaluate_router()