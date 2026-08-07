from .config import TOP_N
from .vector_store import (
    embedding_texts,
    get_collection,
    get_vector_store,
)


def validate_query(query):
    if not isinstance(query, str):
        raise TypeError("Query must be a string")

    query = " ".join(query.strip().split())

    if not query:
        raise ValueError("Query cannot be empty")

    return query


def validate_top_n(top_n):
    if not isinstance(top_n, int):
        raise TypeError("top_n must be an integer")

    if top_n <= 0:
        raise ValueError("top_n must be greater than zero")

    return top_n


def normalize_condition_codes(condition_code=None, condition_codes=None):
    normalized_condition_codes = []

    if condition_code is not None:
        if not isinstance(condition_code, str):
            raise TypeError("condition_code must be a string")

        condition_code = condition_code.strip().lower()

        if condition_code:
            normalized_condition_codes.append(condition_code)

    if condition_codes is not None:
        if isinstance(condition_codes, str):
            condition_codes = [condition_codes]

        if not isinstance(condition_codes, (list, tuple, set)):
            raise TypeError("condition_codes must be a list, tuple or set")

        for current_condition_code in condition_codes:
            if not isinstance(current_condition_code, str):
                raise TypeError("Every condition code must be a string")

            current_condition_code = current_condition_code.strip().lower()

            if current_condition_code and current_condition_code not in normalized_condition_codes:
                normalized_condition_codes.append(current_condition_code)

    return normalized_condition_codes


def convert_search_results_to_chunks(results):
    retrieved_chunks = []

    for doc, score in results:
        distance = float(score)
        metadata = doc.metadata or {}
        chunk_id = getattr(doc, "id", None) or metadata.get("chunk_id") or ""
        condition_code = str(metadata.get("condition_code") or "").strip().lower()

        retrieved_chunks.append(
            {
                "chunk_id": chunk_id,
                "condition_code": condition_code,
                "source_id": metadata.get("source_id"),
                "content": doc.page_content,
                "distance": distance,
                "similarity": 1 - distance,
            }
        )

    return retrieved_chunks


def build_retrieved_chunks_from_raw(results):
    retrieved_chunks = []

    if not results.get("ids") or not results["ids"][0]:
        return retrieved_chunks

    result_ids = results["ids"][0]
    result_documents = results["documents"][0]
    result_metadatas = results["metadatas"][0]
    result_distances = results["distances"][0]

    for index in range(len(result_ids)):
        distance = float(result_distances[index])
        metadata = result_metadatas[index] or {}

        retrieved_chunks.append(
            {
                "chunk_id": result_ids[index],
                "condition_code": str(metadata.get("condition_code") or "").strip().lower(),
                "source_id": metadata.get("source_id"),
                "content": result_documents[index],
                "distance": distance,
                "similarity": 1 - distance,
            }
        )

    return retrieved_chunks


def query_vector_store(query, top_n, condition_code=None):
    collection = get_collection()

    if hasattr(collection, "query") and type(collection).__name__ == "FakeCollection":
        query_embedding = embedding_texts([query])[0]
        query_embedding_data = (
            query_embedding.tolist()
            if hasattr(query_embedding, "tolist")
            else list(query_embedding)
        )

        query_data = {
            "query_embeddings": [query_embedding_data],
            "n_results": top_n,
            "include": ["documents", "metadatas", "distances"],
        }

        if condition_code:
            query_data["where"] = {"condition_code": condition_code}

        results = collection.query(**query_data)

        return build_retrieved_chunks_from_raw(results)

    filter_dict = None

    if condition_code:
        filter_dict = {"condition_code": condition_code}

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_n,
        filter=filter_dict,
    )

    return convert_search_results_to_chunks(results)


def merge_retrieved_chunks(retrieved_chunks):
    chunks_by_id = {}

    for retrieved_chunk in retrieved_chunks:
        chunk_id = retrieved_chunk["chunk_id"]

        if chunk_id not in chunks_by_id:
            chunks_by_id[chunk_id] = retrieved_chunk
            continue

        current_chunk = chunks_by_id[chunk_id]

        if retrieved_chunk["distance"] < current_chunk["distance"]:
            chunks_by_id[chunk_id] = retrieved_chunk

    merged_chunks = list(chunks_by_id.values())

    merged_chunks = sorted(
        merged_chunks,
        key=lambda chunk: (
            chunk["distance"],
            chunk["condition_code"],
            chunk["chunk_id"],
        ),
    )

    for index, retrieved_chunk in enumerate(merged_chunks, start=1):
        retrieved_chunk["rank"] = index

    return merged_chunks


def retrieve(query, top_n=TOP_N, condition_code=None, condition_codes=None):
    query = validate_query(query)
    top_n = validate_top_n(top_n)
    normalized_condition_codes = normalize_condition_codes(
        condition_code=condition_code,
        condition_codes=condition_codes,
    )

    if not normalized_condition_codes:
        retrieved_chunks = query_vector_store(
            query=query,
            top_n=top_n,
        )

        return merge_retrieved_chunks(retrieved_chunks)

    all_retrieved_chunks = []

    for current_condition_code in normalized_condition_codes:
        condition_chunks = query_vector_store(
            query=query,
            top_n=top_n,
            condition_code=current_condition_code,
        )

        all_retrieved_chunks.extend(condition_chunks)

    return merge_retrieved_chunks(all_retrieved_chunks)