from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage

from context_builder import build_context
from health_answer_generator import (
    format_llm_inputs,
    generate_health_answer,
)


def test_format_llm_inputs():
    context_data = {
        "query": "Tôi bị béo phì nên giảm cân thế nào?",
        "primary_route": "condition",
        "conditions": ["obesity"],
        "safety_flags": [],
        "safety_instructions": [],
        "knowledge_context": "Giảm cân từ 5% đến 10% mang lại lợi ích.",
    }

    inputs = format_llm_inputs(context_data)

    assert inputs["query"] == context_data["query"]
    assert inputs["primary_route"] == "condition"
    assert inputs["condition_text"] == "obesity"
    assert inputs["safety_flag_text"] == "Không có"
    assert "- Không có chỉ dẫn an toàn bổ sung." in inputs["safety_instruction_text"]
    assert inputs["knowledge_context"] == context_data["knowledge_context"]


def test_generate_health_answer_with_mock_llm():
    rag_result = {
        "query": "Tôi bị béo phì thì nên giảm cân thế nào?",
        "conditions": ["obesity"],
        "safety_flags": [],
        "primary_route": "condition",
        "retrieved_chunks": [
            {
                "chunk_id": "obesity_001",
                "condition_code": "obesity",
                "source_id": "source_obesity",
                "content": "Giảm cân bền vững bằng cách cắt giảm calo hợp lý.",
                "similarity": 0.85,
            },
        ],
    }

    context_data = build_context(rag_result)

    mock_llm = FakeMessagesListChatModel(
        responses=[
            AIMessage(
                content="Bạn nên giảm cân từ từ bằng cách tạo thâm hụt calo nhẹ nhàng."
            ),
        ]
    )

    result = generate_health_answer(
        context_data=context_data,
        llm=mock_llm,
    )

    assert isinstance(result, dict)
    assert result["answer"] == "Bạn nên giảm cân từ từ bằng cách tạo thâm hụt calo nhẹ nhàng."
    assert result["context_data"] == context_data


def test_generate_health_answer_validates_inputs():
    try:
        generate_health_answer("invalid")
        raise AssertionError("Expected TypeError was not raised")
    except TypeError as error:
        assert str(error) == "context_data must be a dictionary"

    try:
        generate_health_answer({"query": ""})
        raise AssertionError("Expected ValueError was not raised")
    except ValueError as error:
        assert str(error) == "context_data is missing query"


test_cases = [
    (
        "format llm inputs",
        test_format_llm_inputs,
    ),
    (
        "generate health answer with mock llm",
        test_generate_health_answer_with_mock_llm,
    ),
    (
        "generate health answer validates inputs",
        test_generate_health_answer_validates_inputs,
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
    f"HEALTH ANSWER GENERATOR TEST: PASS "
    f"({passed_count}/{len(test_cases)})"
)
