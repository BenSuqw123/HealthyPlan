from django.shortcuts import get_object_or_404

from healthplanapp.models import ConsultationSession, ConsultationMessage
from healthplanapp.services.consultation.profile_context import build_health_context
from healthplanapp.services.consultation.conversation_history import get_recent_conversation_history
from rag.rag_pipeline import run_rag_pipeline


def prepare_consultation(user, content, session_id=None):
    if session_id:
        session = get_object_or_404(ConsultationSession, id=session_id, user=user)
    else:
        session = ConsultationSession.objects.create(user=user)

    conversation_history = get_recent_conversation_history(session)
    health_context = build_health_context(user)

    rag_result = run_rag_pipeline(
        query=content,
        health_context=health_context,
        conversation_history=conversation_history
    )

    ConsultationMessage.objects.create(
        session=session,
        role="user",
        content=content,
        profile_snapshot=health_context
    )

    assistant_message = ConsultationMessage.objects.create(
        session=session,
        role="assistant",
        content=rag_result["answer"],
        profile_snapshot=health_context,
        citations=rag_result["context_data"].get("source_references", []),
        safety_metadata={
            "primary_route": rag_result.get("primary_route"),
            "safety_flags": rag_result.get("safety_flags", [])
        }
    )

    return assistant_message