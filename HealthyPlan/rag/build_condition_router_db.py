from pathlib import Path

import pandas as pd

from config import Path_Root, CONDITION_ROUTER_COLLECTION_NAME
from vector_store import get_chroma_client, embedding_texts


CONDITION_ROUTER_DATA_PATH = f"{Path_Root}/data/rag/condition_router_examples_reviewed.csv"

REQUIRED_COLUMNS = ["example_id", "query", "condition_code", "language", "example_type", "source_chunk_ids", "review_status", "notes"]

EXPECTED_EXAMPLE_COUNT = 320
EXPECTED_CONDITION_COUNT = 16
EXPECTED_EXAMPLES_PER_CONDITION = 20
INSERT_BATCH_SIZE = 100


def load_router_examples():
    data_path = Path(CONDITION_ROUTER_DATA_PATH)

    if not data_path.exists():
        raise FileNotFoundError(f"Router dataset not found: {data_path}")

    dataframe = pd.read_csv(data_path, encoding="utf-8-sig")

    if dataframe.empty:
        raise ValueError("Router dataset is empty")

    dataframe.columns = dataframe.columns.str.strip()

    missing_columns = []

    for column_name in REQUIRED_COLUMNS:
        if column_name not in dataframe.columns:
            missing_columns.append(column_name)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    router_dataframe = dataframe.copy()

    router_dataframe["example_id"] = router_dataframe["example_id"].fillna("").astype(str).str.strip()
    router_dataframe["query"] = router_dataframe["query"].fillna("").astype(str).str.strip()
    router_dataframe["condition_code"] = router_dataframe["condition_code"].fillna("").astype(str).str.strip().str.lower()
    router_dataframe["language"] = router_dataframe["language"].fillna("").astype(str).str.strip().str.lower()
    router_dataframe["example_type"] = router_dataframe["example_type"].fillna("").astype(str).str.strip()
    router_dataframe["source_chunk_ids"] = router_dataframe["source_chunk_ids"].fillna("").astype(str).str.strip()
    router_dataframe["review_status"] = router_dataframe["review_status"].fillna("").astype(str).str.strip()
    router_dataframe["notes"] = router_dataframe["notes"].fillna("").astype(str).str.strip()

    required_value_columns = ["example_id", "query", "condition_code", "language", "example_type", "source_chunk_ids", "review_status"]

    missing_value_rows = router_dataframe[required_value_columns].eq("").any(axis=1)

    if missing_value_rows.any():
        invalid_rows = router_dataframe.loc[missing_value_rows, required_value_columns]
        raise ValueError(f"Rows with missing required values:\n{invalid_rows.to_string(index=False)}")

    duplicated_ids = router_dataframe["example_id"].duplicated(keep=False)

    if duplicated_ids.any():
        duplicate_values = router_dataframe.loc[duplicated_ids, "example_id"].tolist()
        raise ValueError(f"Duplicate example_id values found: {duplicate_values}")

    duplicated_queries = router_dataframe["query"].str.lower().duplicated(keep=False)

    if duplicated_queries.any():
        duplicate_values = router_dataframe.loc[duplicated_queries, ["example_id", "query"]]
        raise ValueError(f"Duplicate query values found:\n{duplicate_values.to_string(index=False)}")

    if len(router_dataframe) != EXPECTED_EXAMPLE_COUNT:
        raise ValueError(f"Expected {EXPECTED_EXAMPLE_COUNT} examples but found {len(router_dataframe)}")

    condition_counts = router_dataframe["condition_code"].value_counts().sort_index()

    if len(condition_counts) != EXPECTED_CONDITION_COUNT:
        raise ValueError(f"Expected {EXPECTED_CONDITION_COUNT} conditions but found {len(condition_counts)}")

    invalid_condition_counts = condition_counts[condition_counts != EXPECTED_EXAMPLES_PER_CONDITION]

    if not invalid_condition_counts.empty:
        raise ValueError(f"Each condition must have {EXPECTED_EXAMPLES_PER_CONDITION} examples:\n{invalid_condition_counts}")

    invalid_languages = router_dataframe[router_dataframe["language"] != "vi"]

    if not invalid_languages.empty:
        raise ValueError("All router examples must use language='vi'")

    invalid_review_statuses = router_dataframe[router_dataframe["review_status"] != "auto_validated"]

    if not invalid_review_statuses.empty:
        raise ValueError("All router examples must use review_status='auto_validated'")

    router_dataframe = router_dataframe.sort_values(by=["condition_code", "example_id"]).reset_index(drop=True)

    return router_dataframe


def create_condition_router_collection():
    client = get_chroma_client()

    collection_names = []

    for collection in client.list_collections():
        if isinstance(collection, str):
            collection_names.append(collection)
        else:
            collection_names.append(collection.name)

    if CONDITION_ROUTER_COLLECTION_NAME in collection_names:
        client.delete_collection(name=CONDITION_ROUTER_COLLECTION_NAME)
        print(f"Deleted old collection: {CONDITION_ROUTER_COLLECTION_NAME}")

    collection = client.create_collection(name=CONDITION_ROUTER_COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

    return collection


def build_condition_router_db():
    router_dataframe = load_router_examples()

    documents = router_dataframe["query"].tolist()
    ids = router_dataframe["example_id"].tolist()

    metadatas = []

    for index in router_dataframe.index:
        metadata = {
            "example_id": router_dataframe.at[index, "example_id"],
            "condition_code": router_dataframe.at[index, "condition_code"],
            "language": router_dataframe.at[index, "language"],
            "example_type": router_dataframe.at[index, "example_type"],
            "source_chunk_ids": router_dataframe.at[index, "source_chunk_ids"],
            "review_status": router_dataframe.at[index, "review_status"],
        }

        metadatas.append(metadata)

    print(f"Router dataset: {CONDITION_ROUTER_DATA_PATH}")
    print(f"Loaded router examples: {len(documents)}")
    print(f"Conditions: {router_dataframe['condition_code'].nunique()}")

    embeddings = embedding_texts(documents)

    if len(embeddings) != len(documents):
        raise ValueError(f"Embedding count mismatch: {len(embeddings)} embeddings for {len(documents)} documents")

    collection = create_condition_router_collection()

    for start_index in range(0, len(documents), INSERT_BATCH_SIZE):
        end_index = min(start_index + INSERT_BATCH_SIZE, len(documents))

        collection.add(
            ids=ids[start_index:end_index],
            documents=documents[start_index:end_index],
            metadatas=metadatas[start_index:end_index],
            embeddings=embeddings[start_index:end_index].tolist(),
        )

        print(f"Inserted examples: {start_index + 1} - {end_index}")

    collection_count = collection.count()

    if collection_count != len(documents):
        raise ValueError(f"Collection count mismatch: expected {len(documents)}, found {collection_count}")

    print("=" * 60)
    print("CONDITION ROUTER VECTOR DATABASE CREATED")
    print(f"Collection: {collection.name}")
    print(f"Total examples: {collection_count}")
    print("Validation: PASS")
    print("=" * 60)


if __name__ == "__main__":
    build_condition_router_db()