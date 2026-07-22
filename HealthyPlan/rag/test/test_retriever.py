from unittest.mock import patch

from retriever import (
    normalize_condition_codes,
    retrieve,
    validate_query,
    validate_top_n,
)


def create_results(chunks):
    ids = []
    documents = []
    metadatas = []
    distances = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["content"])
        metadatas.append(chunk.get("metadata"))
        distances.append(chunk["distance"])

    return {
        "ids": [ids],
        "documents": [documents],
        "metadatas": [metadatas],
        "distances": [distances],
    }


class FakeCollection:
    def __init__(self, results_by_condition=None, default_results=None):
        self.results_by_condition = results_by_condition or {}
        self.default_results = default_results or create_results([])
        self.calls = []

    def query(self, **query_data):
        self.calls.append(query_data)

        where = query_data.get("where")

        if not where:
            return self.default_results

        condition_code = where.get("condition_code")

        return self.results_by_condition.get(
            condition_code,
            create_results([]),
        )


def test_validate_query_normalizes_spaces():
    actual_query = validate_query(
        "   Tôi   bị   suy thận   G3b   "
    )

    expected_query = "Tôi bị suy thận G3b"

    assert actual_query == expected_query, (
        f"Expected: {expected_query}\n"
        f"Actual: {actual_query}"
    )


def test_validate_query_rejects_non_string():
    try:
        validate_query(123)
        raise AssertionError("Expected TypeError was not raised")
    except TypeError as error:
        assert str(error) == "Query must be a string"


def test_validate_query_rejects_empty_query():
    try:
        validate_query("    ")
        raise AssertionError("Expected ValueError was not raised")
    except ValueError as error:
        assert str(error) == "Query cannot be empty"


def test_validate_top_n_accepts_positive_integer():
    assert validate_top_n(5) == 5


def test_validate_top_n_rejects_invalid_value():
    invalid_values = [
        0,
        -1,
        1.5,
        "3",
        None,
    ]

    for invalid_value in invalid_values:
        try:
            validate_top_n(invalid_value)
            raise AssertionError(
                f"Expected validation error for top_n={invalid_value}"
            )
        except (TypeError, ValueError):
            pass


def test_normalize_single_condition_code():
    actual_condition_codes = normalize_condition_codes(
        condition_code="  CKD_G3B  ",
    )

    assert actual_condition_codes == ["ckd_g3b"]


def test_normalize_multiple_condition_codes():
    actual_condition_codes = normalize_condition_codes(
        condition_code="OBESITY",
        condition_codes=[
            "diabetes_type_2",
            " obesity ",
            "DIABETES_TYPE_2",
            "",
        ],
    )

    expected_condition_codes = [
        "obesity",
        "diabetes_type_2",
    ]

    assert actual_condition_codes == expected_condition_codes, (
        f"Expected: {expected_condition_codes}\n"
        f"Actual: {actual_condition_codes}"
    )


def test_retrieve_without_condition_filter():
    default_results = create_results(
        [
            {
                "chunk_id": "chunk_2",
                "content": "Kiến thức thứ hai",
                "metadata": {
                    "condition_code": "hypertension",
                    "source_id": "source_2",
                },
                "distance": 0.30,
            },
            {
                "chunk_id": "chunk_1",
                "content": "Kiến thức thứ nhất",
                "metadata": {
                    "condition_code": "gout",
                    "source_id": "source_1",
                },
                "distance": 0.10,
            },
        ]
    )

    fake_collection = FakeCollection(
        default_results=default_results,
    )

    with patch(
        "retriever.embedding_texts",
        return_value=[[0.1, 0.2, 0.3]],
    ), patch(
        "retriever.get_collection",
        return_value=fake_collection,
    ):
        retrieved_chunks = retrieve(
            query="Tôi nên ăn gì?",
            top_n=2,
        )

    assert len(fake_collection.calls) == 1

    query_data = fake_collection.calls[0]

    assert "where" not in query_data
    assert query_data["n_results"] == 2
    assert query_data["query_embeddings"] == [
        [0.1, 0.2, 0.3]
    ]

    assert [
        chunk["chunk_id"]
        for chunk in retrieved_chunks
    ] == [
        "chunk_1",
        "chunk_2",
    ]

    assert [
        chunk["rank"]
        for chunk in retrieved_chunks
    ] == [
        1,
        2,
    ]


def test_retrieve_with_legacy_condition_code():
    ckd_results = create_results(
        [
            {
                "chunk_id": "ckd_g3b_001",
                "content": "Hạn chế kali phụ thuộc kết quả xét nghiệm.",
                "metadata": {
                    "condition_code": "ckd_g3b",
                    "source_id": "ckd_source",
                },
                "distance": 0.12,
            },
            {
                "chunk_id": "ckd_g3b_002",
                "content": "Không nên tự ý kiêng kali hoàn toàn.",
                "metadata": {
                    "condition_code": "ckd_g3b",
                    "source_id": "ckd_source",
                },
                "distance": 0.20,
            },
        ]
    )

    fake_collection = FakeCollection(
        results_by_condition={
            "ckd_g3b": ckd_results,
        }
    )

    with patch(
        "retriever.embedding_texts",
        return_value=[[0.4, 0.5]],
    ), patch(
        "retriever.get_collection",
        return_value=fake_collection,
    ):
        retrieved_chunks = retrieve(
            query="Suy thận G3b có cần kiêng chuối không?",
            top_n=2,
            condition_code="CKD_G3B",
        )

    assert len(fake_collection.calls) == 1

    assert fake_collection.calls[0]["where"] == {
        "condition_code": "ckd_g3b",
    }

    assert len(retrieved_chunks) == 2
    assert retrieved_chunks[0]["condition_code"] == "ckd_g3b"
    assert retrieved_chunks[0]["chunk_id"] == "ckd_g3b_001"
    assert abs(retrieved_chunks[0]["similarity"] - 0.88) < 0.000001


def test_retrieve_multiple_conditions():
    obesity_results = create_results(
        [
            {
                "chunk_id": "obesity_001",
                "content": "Giảm cân cần tạo thâm hụt năng lượng hợp lý.",
                "metadata": {
                    "condition_code": "obesity",
                    "source_id": "obesity_source",
                },
                "distance": 0.10,
            },
            {
                "chunk_id": "shared_001",
                "content": "Giảm cân cần được thực hiện an toàn.",
                "metadata": {
                    "condition_code": "obesity",
                    "source_id": "shared_source",
                },
                "distance": 0.30,
            },
        ]
    )

    diabetes_results = create_results(
        [
            {
                "chunk_id": "diabetes_001",
                "content": "Theo dõi đường huyết trong quá trình giảm cân.",
                "metadata": {
                    "condition_code": "diabetes_type_2",
                    "source_id": "diabetes_source",
                },
                "distance": 0.15,
            },
            {
                "chunk_id": "shared_001",
                "content": "Giảm cân cần được thực hiện an toàn.",
                "metadata": {
                    "condition_code": "diabetes_type_2",
                    "source_id": "shared_source",
                },
                "distance": 0.20,
            },
        ]
    )

    fake_collection = FakeCollection(
        results_by_condition={
            "obesity": obesity_results,
            "diabetes_type_2": diabetes_results,
        }
    )

    with patch(
        "retriever.embedding_texts",
        return_value=[[0.2, 0.8]],
    ), patch(
        "retriever.get_collection",
        return_value=fake_collection,
    ):
        retrieved_chunks = retrieve(
            query="Tôi bị béo phì và tiểu đường type 2, nên giảm cân thế nào?",
            top_n=2,
            condition_codes=[
                "obesity",
                "diabetes_type_2",
                "OBESITY",
            ],
        )

    assert len(fake_collection.calls) == 2

    called_conditions = [
        call["where"]["condition_code"]
        for call in fake_collection.calls
    ]

    assert called_conditions == [
        "obesity",
        "diabetes_type_2",
    ]

    expected_chunk_ids = [
        "obesity_001",
        "diabetes_001",
        "shared_001",
    ]

    actual_chunk_ids = [
        chunk["chunk_id"]
        for chunk in retrieved_chunks
    ]

    assert actual_chunk_ids == expected_chunk_ids, (
        f"Expected: {expected_chunk_ids}\n"
        f"Actual: {actual_chunk_ids}"
    )

    assert len(retrieved_chunks) == 3

    shared_chunk = next(
        chunk
        for chunk in retrieved_chunks
        if chunk["chunk_id"] == "shared_001"
    )

    assert shared_chunk["distance"] == 0.20
    assert shared_chunk["condition_code"] == "diabetes_type_2"

    assert [
        chunk["rank"]
        for chunk in retrieved_chunks
    ] == [
        1,
        2,
        3,
    ]


def test_retrieve_returns_empty_list():
    fake_collection = FakeCollection(
        results_by_condition={
            "ckd_g1": create_results([]),
        }
    )

    with patch(
        "retriever.embedding_texts",
        return_value=[[0.1, 0.1]],
    ), patch(
        "retriever.get_collection",
        return_value=fake_collection,
    ):
        retrieved_chunks = retrieve(
            query="Câu hỏi không có kết quả",
            condition_code="ckd_g1",
        )

    assert retrieved_chunks == []


def test_retrieve_handles_missing_metadata():
    results = create_results(
        [
            {
                "chunk_id": "missing_metadata_001",
                "content": "Chunk không có metadata.",
                "metadata": None,
                "distance": 0.25,
            },
        ]
    )

    fake_collection = FakeCollection(
        default_results=results,
    )

    with patch(
        "retriever.embedding_texts",
        return_value=[[0.3, 0.7]],
    ), patch(
        "retriever.get_collection",
        return_value=fake_collection,
    ):
        retrieved_chunks = retrieve(
            query="Kiểm tra metadata",
            top_n=1,
        )

    assert len(retrieved_chunks) == 1
    assert retrieved_chunks[0]["condition_code"] == ""
    assert retrieved_chunks[0]["source_id"] is None
    assert retrieved_chunks[0]["content"] == "Chunk không có metadata."


test_cases = [
    (
        "validate query normalizes spaces",
        test_validate_query_normalizes_spaces,
    ),
    (
        "validate query rejects non-string",
        test_validate_query_rejects_non_string,
    ),
    (
        "validate query rejects empty query",
        test_validate_query_rejects_empty_query,
    ),
    (
        "validate top_n accepts positive integer",
        test_validate_top_n_accepts_positive_integer,
    ),
    (
        "validate top_n rejects invalid values",
        test_validate_top_n_rejects_invalid_value,
    ),
    (
        "normalize single condition code",
        test_normalize_single_condition_code,
    ),
    (
        "normalize multiple condition codes",
        test_normalize_multiple_condition_codes,
    ),
    (
        "retrieve without condition filter",
        test_retrieve_without_condition_filter,
    ),
    (
        "retrieve with legacy condition code",
        test_retrieve_with_legacy_condition_code,
    ),
    (
        "retrieve multiple conditions",
        test_retrieve_multiple_conditions,
    ),
    (
        "retrieve returns empty list",
        test_retrieve_returns_empty_list,
    ),
    (
        "retrieve handles missing metadata",
        test_retrieve_handles_missing_metadata,
    ),
]


passed_count = 0

for test_index, test_case in enumerate(test_cases, start=1):
    test_name, test_function = test_case

    try:
        test_function()
        passed_count += 1
        print(f"PASS #{test_index}: {test_name}")
    except Exception as error:
        print(f"FAIL #{test_index}: {test_name}")
        raise error


print(
    f"RETRIEVER TEST: PASS "
    f"({passed_count}/{len(test_cases)})"
)