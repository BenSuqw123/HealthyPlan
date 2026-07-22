from langchain_core.prompts import ChatPromptTemplate

GENERAL_SAFETY_INSTRUCTIONS = [
    "Không chẩn đoán bệnh hoặc khẳng định tình trạng sức khỏe của người dùng.",
    "Không đề xuất người dùng tự ý bắt đầu, ngừng hoặc thay đổi liều thuốc.",
    "Không tự tạo ra chỉ số, liều lượng hoặc giới hạn dinh dưỡng nếu kiến thức tham khảo không cung cấp.",
    "Nêu rõ khi thông tin người dùng cung cấp chưa đủ để đưa ra khuyến nghị cụ thể.",
    "Khuyến nghị người dùng trao đổi với bác sĩ hoặc chuyên gia dinh dưỡng khi có yếu tố rủi ro.",
]


SAFETY_FLAG_INSTRUCTIONS = {
    "pregnancy": [
        "Người dùng đang mang thai hoặc thuộc nhóm thai phụ.",
        "Không tạo thực đơn hạn chế năng lượng hoặc giảm cân chi tiết nếu chưa có đánh giá chuyên môn.",
        "Khuyến nghị trao đổi với bác sĩ sản khoa hoặc chuyên gia dinh dưỡng.",
    ],
    "elderly_frailty": [
        "Người dùng cao tuổi và có nguy cơ suy yếu hoặc mất khối cơ.",
        "Không khuyến nghị giảm cân nhanh hoặc kiêng khem quá mức.",
        "Ưu tiên cảnh báo nguy cơ mất cơ và suy dinh dưỡng.",
    ],
    "conflicting_diet_rules": [
        "Câu hỏi chứa các nguyên tắc ăn uống có thể xung đột.",
        "Không tự chọn một quy tắc ăn uống nếu thiếu dữ liệu xét nghiệm hoặc đánh giá chuyên môn.",
        "Giải thích rõ nguyên nhân cần cá nhân hóa chế độ ăn.",
    ],
    "inconsistent_lab_results": [
        "Các kết quả xét nghiệm người dùng cung cấp không thống nhất.",
        "Không suy luận giai đoạn bệnh từ các kết quả mâu thuẫn.",
        "Khuyến nghị kiểm tra lại kết quả và trao đổi với nhân viên y tế.",
    ],
    "medication_risk": [
        "Câu hỏi liên quan đến việc tự thay đổi thuốc hoặc liều thuốc.",
        "Không đưa hướng dẫn thay đổi thuốc hoặc liều lượng.",
        "Khuyến nghị người dùng liên hệ bác sĩ hoặc dược sĩ.",
    ],
    "malnutrition_risk": [
        "Người dùng có dấu hiệu hoặc nguy cơ suy dinh dưỡng, mất cơ hoặc suy kiệt.",
        "Không khuyến nghị tiếp tục giảm cân hoặc kiêng khem nghiêm ngặt.",
        "Khuyến nghị đánh giá dinh dưỡng bởi nhân viên y tế.",
    ],
    "possible_emergency": [
        "Câu hỏi có dấu hiệu có thể cần chăm sóc y tế khẩn cấp.",
        "Ưu tiên hướng dẫn người dùng tìm hỗ trợ y tế ngay.",
        "Không tiếp tục đưa lời khuyên ăn uống thông thường như câu trả lời chính.",
    ],
    "multiple_conditions": [
        "Người dùng có nhiều tình trạng sức khỏe cùng lúc.",
        "Câu trả lời phải xem xét toàn bộ các condition được cung cấp.",
        "Không đưa lời khuyên phù hợp với một bệnh nhưng có thể gây bất lợi cho bệnh còn lại.",
    ],
}


def validate_rag_result(rag_result):
    if not isinstance(rag_result, dict):
        raise TypeError("rag_result must be a dictionary")

    if not rag_result.get("query"):
        raise ValueError("rag_result is missing query")

    if "retrieved_chunks" not in rag_result:
        raise ValueError("rag_result is missing retrieved_chunks")

    if not isinstance(rag_result["retrieved_chunks"], list):
        raise TypeError("retrieved_chunks must be a list")

    return rag_result


def normalize_string_list(values):
    if not isinstance(values, list):
        return []

    normalized_values = []

    for value in values:
        normalized_value = str(value or "").strip()

        if normalized_value and normalized_value not in normalized_values:
            normalized_values.append(normalized_value)

    return normalized_values


def get_safety_instructions(primary_route, safety_flags):
    safety_instructions = []

    if primary_route == "general_safety" or safety_flags:
        safety_instructions.extend(GENERAL_SAFETY_INSTRUCTIONS)

    for safety_flag in safety_flags:
        flag_instructions = SAFETY_FLAG_INSTRUCTIONS.get(safety_flag, [])

        for instruction in flag_instructions:
            if instruction not in safety_instructions:
                safety_instructions.append(instruction)

    return safety_instructions


def build_knowledge_context(retrieved_chunks):
    context_parts = []
    source_references = []

    for index, retrieved_chunk in enumerate(retrieved_chunks, start=1):
        content = str(retrieved_chunk.get("content") or "").strip()

        if not content:
            continue

        chunk_id = str(retrieved_chunk.get("chunk_id") or "").strip()
        condition_code = str(retrieved_chunk.get("condition_code") or "").strip()
        source_id = str(retrieved_chunk.get("source_id") or "").strip()
        similarity = float(retrieved_chunk.get("similarity", 0.0))

        context_parts.append(
            f"[Knowledge {index}]\n"
            f"Condition: {condition_code}\n"
            f"Chunk ID: {chunk_id}\n"
            f"Content: {content}"
        )

        source_references.append(
            {
                "number": index,
                "chunk_id": chunk_id,
                "condition_code": condition_code,
                "source_id": source_id,
                "similarity": similarity,
            }
        )

    return {
        "knowledge_context": "\n\n".join(context_parts),
        "source_references": source_references,
    }


def get_rag_chat_prompt_template():
    system_template = (
        "Bạn là trợ lý tư vấn sức khỏe của hệ thống HealthyPlan.\n\n"
        "Chỉ dẫn an toàn:\n"
        "{safety_instruction_text}\n\n"
        "Kiến thức tham khảo:\n"
        "{knowledge_context}\n\n"
        "Yêu cầu trả lời:\n"
        "- Trả lời bằng tiếng Việt rõ ràng, dễ hiểu.\n"
        "- Chỉ sử dụng kiến thức tham khảo được cung cấp.\n"
        "- Không tự chẩn đoán hoặc khẳng định tình trạng sức khỏe.\n"
        "- Không tự tạo số liệu hoặc giới hạn dinh dưỡng nếu kiến thức tham khảo không cung cấp.\n"
        "- Không hướng dẫn tự thay đổi thuốc hoặc liều thuốc.\n"
        "- Phải xem xét toàn bộ các condition được cung cấp.\n"
        "- Phải tuân thủ các chỉ dẫn an toàn và safety flags.\n"
        "- Khi thiếu thông tin, phải nói rõ thông tin nào còn thiếu.\n"
        "- Kết thúc bằng lời khuyên an toàn phù hợp khi có safety flag."
    )

    human_template = (
        "Câu hỏi người dùng:\n"
        "{query}\n\n"
        "Thông tin định tuyến:\n"
        "- Primary route: {primary_route}\n"
        "- Conditions: {condition_text}\n"
        "- Safety flags: {safety_flag_text}"
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("human", human_template),
        ]
    )


def build_llm_prompt(query, conditions, safety_flags, primary_route, safety_instructions, knowledge_context):
    condition_text = ", ".join(conditions) if conditions else "Không xác định"
    safety_flag_text = ", ".join(safety_flags) if safety_flags else "Không có"

    if safety_instructions:
        safety_instruction_text = "\n".join(
            f"- {instruction}"
            for instruction in safety_instructions
        )
    else:
        safety_instruction_text = "- Không có chỉ dẫn an toàn bổ sung."

    if not knowledge_context:
        knowledge_context = "Không tìm thấy đoạn kiến thức phù hợp."

    prompt_template = get_rag_chat_prompt_template()

    formatted_messages = prompt_template.format_messages(
        query=query,
        primary_route=primary_route,
        condition_text=condition_text,
        safety_flag_text=safety_flag_text,
        safety_instruction_text=safety_instruction_text,
        knowledge_context=knowledge_context,
    )

    return "\n\n".join(
        message.content
        for message in formatted_messages
    )


def build_context(rag_result):
    rag_result = validate_rag_result(rag_result)

    query = str(rag_result["query"]).strip()
    conditions = normalize_string_list(rag_result.get("conditions", []))
    safety_flags = normalize_string_list(rag_result.get("safety_flags", []))
    primary_route = str(rag_result.get("primary_route") or "unknown").strip()

    knowledge_result = build_knowledge_context(
        rag_result["retrieved_chunks"]
    )

    safety_instructions = get_safety_instructions(
        primary_route,
        safety_flags,
    )

    llm_prompt = build_llm_prompt(
        query=query,
        conditions=conditions,
        safety_flags=safety_flags,
        primary_route=primary_route,
        safety_instructions=safety_instructions,
        knowledge_context=knowledge_result["knowledge_context"],
    )

    return {
        "query": query,
        "conditions": conditions,
        "safety_flags": safety_flags,
        "primary_route": primary_route,
        "safety_instructions": safety_instructions,
        "knowledge_context": knowledge_result["knowledge_context"],
        "source_references": knowledge_result["source_references"],
        "source_count": len(knowledge_result["source_references"]),
        "llm_prompt": llm_prompt,
    }