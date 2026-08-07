from .context_builder import (
    GENERAL_SAFETY_INSTRUCTIONS,
    build_context,
    build_knowledge_context,
    get_safety_instructions,
    normalize_string_list,
    validate_rag_result,
)


def test_validate_rag_result_accepts_valid_data():
    rag_result = {
        "query": "Tôi nên ăn gì?",
        "retrieved_chunks": [],
    }

    assert validate_rag_result(rag_result) == rag_result


def test_validate_rag_result_rejects_non_dictionary():
    try:
        validate_rag_result("invalid")
        raise AssertionError("Expected TypeError was not raised")
    except TypeError as error:
        assert str(error) == "rag_result must be a dictionary"


def test_validate_rag_result_rejects_missing_query():
    rag_result = {
        "retrieved_chunks": [],
    }

    try:
        validate_rag_result(rag_result)
        raise AssertionError("Expected ValueError was not raised")
    except ValueError as error:
        assert str(error) == "rag_result is missing query"


def test_validate_rag_result_rejects_missing_chunks():
    rag_result = {
        "query": "Tôi nên ăn gì?",
    }

    try:
        validate_rag_result(rag_result)
        raise AssertionError("Expected ValueError was not raised")
    except ValueError as error:
        assert str(error) == "rag_result is missing retrieved_chunks"


def test_validate_rag_result_rejects_invalid_chunks():
    rag_result = {
        "query": "Tôi nên ăn gì?",
        "retrieved_chunks": "invalid",
    }

    try:
        validate_rag_result(rag_result)
        raise AssertionError("Expected TypeError was not raised")
    except TypeError as error:
        assert str(error) == "retrieved_chunks must be a list"


def test_normalize_string_list():
    values = [
        " obesity ",
        "diabetes_type_2",
        "obesity",
        "",
        None,
    ]

    normalized_values = normalize_string_list(values)

    assert normalized_values == [
        "obesity",
        "diabetes_type_2",
    ]


def test_no_safety_instructions_for_normal_route():
    instructions = get_safety_instructions(
        primary_route="condition",
        safety_flags=[],
    )

    assert instructions == []


def test_general_safety_instructions():
    instructions = get_safety_instructions(
        primary_route="general_safety",
        safety_flags=[],
    )

    assert instructions == GENERAL_SAFETY_INSTRUCTIONS


def test_pregnancy_safety_instructions():
    instructions = get_safety_instructions(
        primary_route="general_safety",
        safety_flags=[
            "pregnancy",
            "multiple_conditions",
        ],
    )

    assert GENERAL_SAFETY_INSTRUCTIONS[0] in instructions

    assert (
        "Không tạo thực đơn hạn chế năng lượng hoặc giảm cân chi tiết "
        "nếu chưa có đánh giá chuyên môn."
        in instructions
    )

    assert (
        "Câu trả lời phải xem xét toàn bộ các condition được cung cấp."
        in instructions
    )

    assert len(instructions) == len(set(instructions))


def test_build_knowledge_context():
    retrieved_chunks = [
        {
            "chunk_id": "obesity_001",
            "condition_code": "obesity",
            "source_id": "source_obesity",
            "content": "Giảm cân từ từ giúp duy trì kết quả lâu dài.",
            "similarity": 0.82,
        },
        {
            "chunk_id": "diabetes_001",
            "condition_code": "diabetes_type_2",
            "source_id": "source_diabetes",
            "content": "Theo dõi đường huyết trong quá trình giảm cân.",
            "similarity": 0.78,
        },
    ]

    result = build_knowledge_context(retrieved_chunks)

    assert "[Knowledge 1]" in result["knowledge_context"]
    assert "[Knowledge 2]" in result["knowledge_context"]
    assert "Condition: obesity" in result["knowledge_context"]
    assert "Condition: diabetes_type_2" in result["knowledge_context"]
    assert "Chunk ID: obesity_001" in result["knowledge_context"]

    assert len(result["source_references"]) == 2

    assert result["source_references"][0] == {
        "number": 1,
        "chunk_id": "obesity_001",
        "condition_code": "obesity",
        "source_id": "source_obesity",
        "similarity": 0.82,
    }


def test_build_knowledge_context_skips_empty_content():
    retrieved_chunks = [
        {
            "chunk_id": "empty_001",
            "condition_code": "obesity",
            "source_id": "source_1",
            "content": "   ",
            "similarity": 0.50,
        },
    ]

    result = build_knowledge_context(retrieved_chunks)

    assert result["knowledge_context"] == ""
    assert result["source_references"] == []


def test_build_context_normal_route():
    rag_result = {
        "query": "Tôi bị béo phì thì nên giảm cân thế nào?",
        "conditions": [
            "obesity",
        ],
        "safety_flags": [],
        "primary_route": "condition",
        "retrieved_chunks": [
            {
                "chunk_id": "obesity_001",
                "condition_code": "obesity",
                "source_id": "source_obesity",
                "content": (
                    "Giảm cân bền vững nên được thực hiện "
                    "thông qua thay đổi ăn uống và vận động."
                ),
                "similarity": 0.85,
            },
        ],
    }

    result = build_context(rag_result)

    assert result["query"] == rag_result["query"]
    assert result["conditions"] == ["obesity"]
    assert result["safety_flags"] == []
    assert result["primary_route"] == "condition"
    assert result["safety_instructions"] == []
    assert result["source_count"] == 1

    assert rag_result["query"] in result["llm_prompt"]
    assert "Conditions: obesity" in result["llm_prompt"]
    assert "Safety flags: Không có" in result["llm_prompt"]
    assert "Giảm cân bền vững" in result["llm_prompt"]


def test_build_context_multiple_conditions():
    rag_result = {
        "query": (
            "Tôi bị béo phì và tiểu đường type 2, "
            "nên giảm cân thế nào?"
        ),
        "conditions": [
            "obesity",
            "diabetes_type_2",
        ],
        "safety_flags": [
            "multiple_conditions",
        ],
        "primary_route": "condition",
        "retrieved_chunks": [
            {
                "chunk_id": "obesity_001",
                "condition_code": "obesity",
                "source_id": "source_obesity",
                "content": (
                    "Giảm cân từ 5% đến 10% trọng lượng cơ thể "
                    "có thể mang lại lợi ích sức khỏe."
                ),
                "similarity": 0.84,
            },
            {
                "chunk_id": "diabetes_001",
                "condition_code": "diabetes_type_2",
                "source_id": "source_diabetes",
                "content": (
                    "Quản lý cân nặng có thể hỗ trợ "
                    "kiểm soát đường huyết."
                ),
                "similarity": 0.79,
            },
        ],
    }

    result = build_context(rag_result)

    assert result["conditions"] == [
        "obesity",
        "diabetes_type_2",
    ]

    assert result["safety_flags"] == [
        "multiple_conditions",
    ]

    assert result["source_count"] == 2

    assert (
        "Câu trả lời phải xem xét toàn bộ các condition được cung cấp."
        in result["safety_instructions"]
    )

    assert (
        "Conditions: obesity, diabetes_type_2"
        in result["llm_prompt"]
    )

    assert (
        "Safety flags: multiple_conditions"
        in result["llm_prompt"]
    )


def test_build_context_general_safety():
    rag_result = {
        "query": "Tôi đang mang thai và bị tiểu đường, nên giảm cân không?",
        "conditions": [
            "diabetes_type_unknown",
        ],
        "safety_flags": [
            "pregnancy",
        ],
        "primary_route": "general_safety",
        "retrieved_chunks": [],
    }

    result = build_context(rag_result)

    assert result["primary_route"] == "general_safety"
    assert result["source_count"] == 0

    assert (
        "Không tìm thấy đoạn kiến thức phù hợp."
        in result["llm_prompt"]
    )

    assert (
        "Không tạo thực đơn hạn chế năng lượng hoặc giảm cân chi tiết"
        in result["llm_prompt"]
    )


test_cases = [
    (
        "validate valid rag result",
        test_validate_rag_result_accepts_valid_data,
    ),
    (
        "reject non-dictionary rag result",
        test_validate_rag_result_rejects_non_dictionary,
    ),
    (
        "reject missing query",
        test_validate_rag_result_rejects_missing_query,
    ),
    (
        "reject missing retrieved chunks",
        test_validate_rag_result_rejects_missing_chunks,
    ),
    (
        "reject invalid retrieved chunks",
        test_validate_rag_result_rejects_invalid_chunks,
    ),
    (
        "normalize string list",
        test_normalize_string_list,
    ),
    (
        "normal route has no safety instructions",
        test_no_safety_instructions_for_normal_route,
    ),
    (
        "general safety instructions",
        test_general_safety_instructions,
    ),
    (
        "pregnancy safety instructions",
        test_pregnancy_safety_instructions,
    ),
    (
        "build knowledge context",
        test_build_knowledge_context,
    ),
    (
        "skip empty knowledge content",
        test_build_knowledge_context_skips_empty_content,
    ),
    (
        "build normal context",
        test_build_context_normal_route,
    ),
    (
        "build multiple-condition context",
        test_build_context_multiple_conditions,
    ),
    (
        "build general-safety context",
        test_build_context_general_safety,
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
    f"CONTEXT BUILDER TEST: PASS "
    f"({passed_count}/{len(test_cases)})"
)