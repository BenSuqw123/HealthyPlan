from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL_NAME,
    OLLAMA_TEMPERATURE,
)
from context_builder import get_rag_chat_prompt_template


def get_ollama_llm(model_name=OLLAMA_MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=OLLAMA_TEMPERATURE):
    return ChatOllama(
        model=model_name,
        base_url=base_url,
        temperature=temperature,
    )


def format_llm_inputs(context_data):
    conditions = context_data.get("conditions", [])
    safety_flags = context_data.get("safety_flags", [])
    safety_instructions = context_data.get("safety_instructions", [])
    knowledge_context = context_data.get("knowledge_context", "")

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

    return {
        "query": str(context_data.get("query", "")).strip(),
        "primary_route": str(context_data.get("primary_route", "unknown")).strip(),
        "condition_text": condition_text,
        "safety_flag_text": safety_flag_text,
        "safety_instruction_text": safety_instruction_text,
        "knowledge_context": knowledge_context,
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
