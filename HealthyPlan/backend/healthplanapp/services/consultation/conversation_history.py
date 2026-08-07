HISTORY_LIMIT = 8


def get_recent_conversation_history(session, limit=HISTORY_LIMIT):
    messages = list(
        session.messages.only("role", "content", "created_at").order_by("-created_at")[:limit]
    )

    messages.reverse()

    return [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]