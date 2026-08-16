from .context_builder import build_context
from .health_answer_generator import generate_health_answer
from .hybrid_condition_router import route_condition_hybrid
from .retriever import retrieve

def get_retrieval_condition_codes(router_result):
    conditions = list(router_result.get("conditions", []))
    condition_code = router_result.get("condition_code")

    if condition_code == "general_safety":
        if "general_safety" not in conditions:
            conditions.append("general_safety")

    elif condition_code and condition_code not in conditions:
        conditions.insert(0, condition_code)

    normalized_conditions = []

    for current_condition in conditions:
        current_condition = str(current_condition or "").strip().lower()

        if current_condition and current_condition not in normalized_conditions:
            normalized_conditions.append(current_condition)

    return normalized_conditions


def run_rag_retrieval(query, top_n=None):
    router_result = route_condition_hybrid(query)
    retrieval_condition_codes = get_retrieval_condition_codes(router_result)

    retrieve_data = {
        "query": query,
        "condition_codes": retrieval_condition_codes,
    }

    if top_n is not None:
        retrieve_data["top_n"] = top_n

    retrieved_chunks = retrieve(**retrieve_data)

    return {
        "query": query,
        "status": router_result["status"],
        "condition_code": router_result["condition_code"],
        "conditions": router_result["conditions"],
        "retrieval_condition_codes": retrieval_condition_codes,
        "safety_flags": router_result["safety_flags"],
        "primary_condition": router_result["primary_condition"],
        "primary_route": router_result["primary_route"],
        "needs_clarification": router_result["needs_clarification"],
        "decision_reason": router_result["decision_reason"],
        "retrieved_chunks": retrieved_chunks,
        "retrieved_chunk_count": len(retrieved_chunks),
        "router_result": router_result,
    }

def build_contextual_query(query, conversation_history=None):
    conversation_history = conversation_history or []

    for message in reversed(conversation_history):
        if message.get("role") == "user":
            previous_query = str(message.get("content") or "").strip()

            if previous_query:
                return f"{previous_query}\n{query}"

    return query
    
def run_rag_pipeline(query, health_context=None,conversation_history=None, top_n=None, llm=None):
    query = build_contextual_query(query, conversation_history)
    rag_retrieval_result = run_rag_retrieval(
        query=query,
        top_n=top_n,
    )

    context_data = build_context(
        rag_result=rag_retrieval_result,
    )

    context_data["health_context"] = health_context or {}
    context_data["conversation_history"] = conversation_history or []

    answer_result = generate_health_answer(
        context_data=context_data,
        llm=llm,
    )

    return {
        "query": query,
        "primary_route": rag_retrieval_result["primary_route"],
        "conditions": rag_retrieval_result["conditions"],
        "safety_flags": rag_retrieval_result["safety_flags"],
        "retrieved_chunks": rag_retrieval_result["retrieved_chunks"],
        "retrieved_chunk_count": rag_retrieval_result["retrieved_chunk_count"],
        "context_data": context_data,
        "answer": answer_result["answer"],
        "rag_retrieval_result": rag_retrieval_result,
    }