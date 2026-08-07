from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from .config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL_NAME,
    OLLAMA_TEMPERATURE,
)
from .context_builder import get_rag_chat_prompt_template


def get_ollama_llm(model_name=OLLAMA_MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=OLLAMA_TEMPERATURE):
    return ChatOllama(
        model=model_name,
        base_url=base_url,
        temperature=temperature,
        keep_alive="1h",
    )


def classify_query_intent(query):
    if not query or not isinstance(query, str):
        return "GENERAL"

    q = query.lower().strip()

    cause_patterns = [
        "tại sao", "vì sao", "nguyên nhân", "do đâu", "lý do",
        "tại sao bị", "tại sao lại bị", "vì sao bị", "nguyên nhân bị",
        "do đâu bị", "nguyên nhân dẫn đến", "tại sao lại"
    ]
    if any(pattern in q for pattern in cause_patterns):
        return "CAUSE"

    advice_patterns = [
        "nêu ăn", "nơi ăn", "nên ăn", "ăn gì", "thực đơn", "chế độ ăn", "kiêng ăn", "dinh dưỡng",
        "nên tập", "tập thế nào", "tập như thế nào", "luyện tập", "vận động",
        "nên làm gì", "cần làm gì", "làm sao để", "cách kiểm soát", "cách điều trị",
        "tư vấn", "lời khuyên", "với tình trạng", "chế độ sinh hoạt", "cải thiện",
        "nên dùng", "thế nào", "như thế nào", "làm gì để"
    ]
    if any(pattern in q for pattern in advice_patterns):
        return "ADVICE"

    return "GENERAL"


def format_llm_inputs(context_data):
    conditions = context_data.get("conditions", [])
    safety_flags = context_data.get("safety_flags", [])
    safety_instructions = context_data.get("safety_instructions", [])
    knowledge_context = context_data.get("knowledge_context", "")
    health_context = context_data.get("health_context", {})
    conversation_history = context_data.get("conversation_history", [])

    condition_text = ", ".join(conditions) if conditions else "Không xác định"
    safety_flag_text = ", ".join(safety_flags) if safety_flags else "Không có"
    
    history_lines = []

    for message in conversation_history:
        role = message.get("role")
        content = str(message.get("content") or "").strip()

        if not content:
            continue

        if role == "user":
            history_lines.append(f"User: {content}")
        elif role == "assistant":
            history_lines.append(f"Assistant: {content}")

    conversation_history_text = "\n".join(history_lines)

    if not conversation_history_text:
        conversation_history_text = "Không có lịch sử hội thoại trước đó."
    if safety_instructions:
        safety_instruction_text = "\n".join(f"- {instruction}" for instruction in safety_instructions)
    else:
        safety_instruction_text = "- Không có chỉ dẫn an toàn bổ sung."

    if not knowledge_context:
        knowledge_context = "Không tìm thấy đoạn kiến thức phù hợp."

    query = str(context_data.get("query", "")).strip()
    intent_mode = classify_query_intent(query)

    health_issues = health_context.get("health_issues", []) if isinstance(health_context, dict) else []
    health_issue_text = ", ".join(issue.get("name", "") for issue in health_issues if issue.get("name")) if health_issues else "Không có"

    if intent_mode == "CAUSE":
        health_context_text = (
            f"- Tuổi: {health_context.get('age', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'}\n"
            f"- Giới tính: {health_context.get('gender', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'}\n"
            f"- Vấn đề sức khỏe đã khai báo: {health_issue_text}\n"
            f"- Vấn đề sức khỏe khác: {(health_context.get('other_health_issue') if isinstance(health_context, dict) else None) or 'Không có'}\n"
            f"- LƯU Ý: Hồ sơ trên chỉ là dữ liệu người dùng khai báo, không phải bằng chứng xác định nguyên nhân gây bệnh cá nhân."
        )
    elif intent_mode == "ADVICE":
        health_context_text = (
            f"- Tuổi: {health_context.get('age', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'}\n"
            f"- Giới tính: {health_context.get('gender', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'}\n"
            f"- Cân nặng: {health_context.get('weight', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'} kg\n"
            f"- Chiều cao: {health_context.get('height', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'} cm\n"
            f"- BMI: {health_context.get('bmi', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'} (chỉ số tính toán, không tự phân loại)\n"
            f"- Mức vận động do người dùng khai báo: {health_context.get('activity_level', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'}\n"
            f"- Mục tiêu cá nhân do người dùng chọn: {health_context.get('goal', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'}\n"
            f"- Cân nặng mục tiêu do người dùng chọn: {health_context.get('target_weight', 'Không có dữ liệu') if isinstance(health_context, dict) else 'Không có dữ liệu'} kg\n"
            f"- Vấn đề sức khỏe đã khai báo: {health_issue_text}\n"
            f"- Vấn đề sức khỏe khác: {(health_context.get('other_health_issue') if isinstance(health_context, dict) else None) or 'Không có'}"
        )
    else:
        health_context_text = "Không áp dụng hồ sơ sức khỏe cá nhân cho câu hỏi thông tin y khoa chung."

    return {
        "query": query,
        "primary_route": str(context_data.get("primary_route", "unknown")).strip(),
        "condition_text": condition_text,
        "safety_flag_text": safety_flag_text,
        "safety_instruction_text": safety_instruction_text,
        "knowledge_context": knowledge_context,
        "health_context": health_context_text,
        "conversation_history": conversation_history_text,
    }


def generate_health_answer(context_data, llm=None):
    if not isinstance(context_data, dict):
        raise TypeError("context_data must be a dictionary")

    if not context_data.get("query"):
        raise ValueError("context_data is missing query")

    if llm is None:
        llm = get_ollama_llm()

    prompt_template = get_rag_chat_prompt_template()
    output_parser = StrOutputParser()

    chain = prompt_template | llm | output_parser

    inputs = format_llm_inputs(
        context_data=context_data,
    )

    answer_text = chain.invoke(
        inputs,
    )

    return {
        "answer": str(answer_text or "").strip(),
        "context_data": context_data,
    }