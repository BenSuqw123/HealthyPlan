from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage

from rag_pipeline import (
    run_rag_pipeline,
    run_rag_retrieval,
)


def test_rag_pipeline_retrieval_pass():
    query = "Tôi bị béo phì và tiểu đường type 2, nên giảm cân thế nào?"

    retrieval_result = run_rag_retrieval(
        query=query,
        top_n=3,
    )

    assert retrieval_result["primary_condition"] == "diabetes_type_2" or retrieval_result["condition_code"] == "diabetes_type_2"
    assert "obesity" in retrieval_result["conditions"]
    assert "diabetes_type_2" in retrieval_result["conditions"]
    assert "multiple_conditions" in retrieval_result["safety_flags"]
    assert retrieval_result["retrieved_chunk_count"] == 6

    obesity_count = sum(
        1 for chunk in retrieval_result["retrieved_chunks"] if chunk["condition_code"] == "obesity"
    )
    diabetes_count = sum(
        1 for chunk in retrieval_result["retrieved_chunks"] if chunk["condition_code"] == "diabetes_type_2"
    )

    assert obesity_count == 3
    assert diabetes_count == 3


def test_rag_pipeline_end_to_end_mock_llm():
    query = "Tôi bị béo phì và tiểu đường type 2, nên giảm cân thế nào?"

    mock_llm = FakeMessagesListChatModel(
        responses=[
            AIMessage(
                content=(
                    "Dựa trên thông tin y tế, người mắc béo phì và đái tháo đường type 2 "
                    "nên giảm cân từ 5% đến 10% trọng lượng cơ thể để cải thiện độ nhạy insulin "
                    "và kiểm soát HbA1c."
                )
            ),
        ]
    )

    pipeline_result = run_rag_pipeline(
        query=query,
        top_n=3,
        llm=mock_llm,
    )

    assert pipeline_result["query"] == query
    assert pipeline_result["primary_route"] in ["condition", "diabetes_type_2"]
    assert "obesity" in pipeline_result["conditions"]
    assert "diabetes_type_2" in pipeline_result["conditions"]
    assert "multiple_conditions" in pipeline_result["safety_flags"]
    assert pipeline_result["retrieved_chunk_count"] == 6
    assert pipeline_result["context_data"]["source_count"] == 6
    assert "Dựa trên thông tin y tế" in pipeline_result["answer"]


test_cases = [
    (
        "rag pipeline retrieval verification",
        test_rag_pipeline_retrieval_pass,
    ),
    (
        "rag pipeline end to end with mock llm",
        test_rag_pipeline_end_to_end_mock_llm,
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
    f"RAG PIPELINE END TO END TEST: PASS "
    f"({passed_count}/{len(test_cases)})"
)
