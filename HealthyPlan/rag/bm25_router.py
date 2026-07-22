import math
from collections import Counter
from functools import lru_cache
from pathlib import Path

import pandas as pd

from config import Path_Root, BM25_K1, BM25_B, BM25_TOP_N, BM25_MAX_NGRAM
from query_processor import process_query


CONDITION_ROUTER_DATA_PATH = f"{Path_Root}/data/rag/condition_router_examples_reviewed.csv"

REQUIRED_COLUMNS = ["example_id", "query", "condition_code", "language", "example_type", "source_chunk_ids", "review_status"]


def tokenize_bm25_text(text):
    processed_query = process_query(text)
    base_tokens = processed_query["router_text"].split()

    if not base_tokens:
        return []

    tokens = list(base_tokens)

    for ngram_size in range(2, BM25_MAX_NGRAM + 1):
        for start_index in range(0, len(base_tokens) - ngram_size + 1):
            end_index = start_index + ngram_size
            ngram_tokens = base_tokens[start_index:end_index]
            ngram = "_".join(ngram_tokens)
            tokens.append(ngram)

    return tokens


@lru_cache(maxsize=1)
def get_bm25_router_index():
    data_path = Path(CONDITION_ROUTER_DATA_PATH)

    if not data_path.exists():
        raise FileNotFoundError(f"Router dataset not found: {data_path}")

    dataframe = pd.read_csv(data_path, encoding="utf-8-sig")

    if dataframe.empty:
        raise ValueError("Router dataset is empty.")

    dataframe.columns = dataframe.columns.str.strip()

    missing_columns = [column_name for column_name in REQUIRED_COLUMNS if column_name not in dataframe.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    for column_name in REQUIRED_COLUMNS:
        dataframe[column_name] = dataframe[column_name].fillna("").astype(str).str.strip()

    missing_value_rows = dataframe[REQUIRED_COLUMNS].eq("").any(axis=1)

    if missing_value_rows.any():
        invalid_rows = dataframe.loc[missing_value_rows, REQUIRED_COLUMNS]
        raise ValueError(f"Rows with missing required values:\n{invalid_rows.to_string(index=False)}")

    duplicated_ids = dataframe["example_id"].duplicated(keep=False)

    if duplicated_ids.any():
        duplicate_values = dataframe.loc[duplicated_ids, "example_id"].tolist()
        raise ValueError(f"Duplicate example_id values found: {duplicate_values}")

    duplicated_queries = dataframe["query"].str.lower().duplicated(keep=False)

    if duplicated_queries.any():
        duplicate_values = dataframe.loc[duplicated_queries, ["example_id", "query"]]
        raise ValueError(f"Duplicate query values found:\n{duplicate_values.to_string(index=False)}")

    dataframe["condition_code"] = dataframe["condition_code"].str.lower()
    dataframe = dataframe.sort_values(by=["condition_code", "example_id"]).reset_index(drop=True)

    document_term_frequencies = []
    document_lengths = []
    document_frequencies = Counter()

    for query in dataframe["query"].tolist():
        tokens = tokenize_bm25_text(query)

        if not tokens:
            raise ValueError(f"Router example produced no BM25 tokens: {query}")

        term_frequencies = Counter(tokens)

        document_term_frequencies.append(term_frequencies)
        document_lengths.append(len(tokens))

        for term in term_frequencies.keys():
            document_frequencies[term] += 1

    total_documents = len(dataframe)

    if total_documents == 0:
        raise ValueError("BM25 router dataset contains no documents.")

    average_document_length = sum(document_lengths) / total_documents

    if average_document_length <= 0:
        raise ValueError("Average BM25 document length must be greater than zero.")

    inverse_document_frequencies = {}

    for term, document_frequency in document_frequencies.items():
        numerator = total_documents - document_frequency + 0.5
        denominator = document_frequency + 0.5
        inverse_document_frequency = math.log(1 + (numerator / denominator))
        inverse_document_frequencies[term] = inverse_document_frequency

    bm25_index = {
        "dataframe": dataframe,
        "document_term_frequencies": document_term_frequencies,
        "document_lengths": document_lengths,
        "document_frequencies": document_frequencies,
        "inverse_document_frequencies": inverse_document_frequencies,
        "total_documents": total_documents,
        "average_document_length": average_document_length,
    }

    print(f"BM25 router index loaded: {total_documents} examples")
    print(f"BM25 vocabulary size: {len(document_frequencies)}")
    print(f"BM25 maximum n-gram size: {BM25_MAX_NGRAM}")

    return bm25_index


def calculate_bm25_document_score(query_tokens, document_term_frequencies, document_length, inverse_document_frequencies, average_document_length):
    score = 0.0
    unique_query_terms = set(query_tokens)

    for query_term in unique_query_terms:
        term_frequency = document_term_frequencies.get(query_term, 0)

        if term_frequency == 0:
            continue

        inverse_document_frequency = inverse_document_frequencies.get(query_term, 0.0)
        length_ratio = document_length / average_document_length
        length_normalization = 1 - BM25_B + BM25_B * length_ratio
        denominator = term_frequency + BM25_K1 * length_normalization

        if denominator <= 0:
            continue

        numerator = term_frequency * (BM25_K1 + 1)
        term_score = inverse_document_frequency * (numerator / denominator)
        score += term_score

    return float(score)


def search_bm25_router(query, top_n=BM25_TOP_N):
    if not isinstance(top_n, int):
        raise ValueError("top_n must be an integer.")

    if top_n <= 0:
        raise ValueError("top_n must be greater than zero.")

    processed_query = process_query(query)
    query_tokens = tokenize_bm25_text(processed_query["normalized_query"])

    if not query_tokens:
        raise ValueError("Query produced no BM25 tokens.")

    bm25_index = get_bm25_router_index()

    dataframe = bm25_index["dataframe"]
    document_term_frequencies = bm25_index["document_term_frequencies"]
    document_lengths = bm25_index["document_lengths"]
    inverse_document_frequencies = bm25_index["inverse_document_frequencies"]
    average_document_length = bm25_index["average_document_length"]

    bm25_results = []

    for index in dataframe.index:
        document_score = calculate_bm25_document_score(query_tokens, document_term_frequencies[index], document_lengths[index], inverse_document_frequencies, average_document_length)

        if document_score <= 0:
            continue

        bm25_result = {
            "example_id": dataframe.at[index, "example_id"],
            "query": dataframe.at[index, "query"],
            "condition_code": dataframe.at[index, "condition_code"],
            "language": dataframe.at[index, "language"],
            "example_type": dataframe.at[index, "example_type"],
            "source_chunk_ids": dataframe.at[index, "source_chunk_ids"],
            "review_status": dataframe.at[index, "review_status"],
            "bm25_score": float(document_score),
        }

        bm25_results.append(bm25_result)

    bm25_results = sorted(bm25_results, key=lambda item: (-item["bm25_score"], item["example_id"]))
    bm25_results = bm25_results[:top_n]

    for rank, bm25_result in enumerate(bm25_results, start=1):
        bm25_result["bm25_rank"] = rank

    search_result = {
        "processed_query": processed_query,
        "query_tokens": query_tokens,
        "returned_match_count": len(bm25_results),
        "bm25_results": bm25_results,
    }

    return search_result