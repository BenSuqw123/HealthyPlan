import re
import unicodedata


def remove_vietnamese_accents(text):
    text = text.replace("đ", "d")
    text = text.replace("Đ", "D")

    normalized_text = unicodedata.normalize("NFD", text)

    accent_free_text = "".join(character for character in normalized_text if unicodedata.category(character) != "Mn")

    return accent_free_text


def process_query(query, max_length=1000):
    if not isinstance(query, str):
        raise ValueError("Query must be a string.")

    original_query = query

    normalized_query = unicodedata.normalize("NFC", query)
    normalized_query = re.sub(r"\s+", " ", normalized_query)
    normalized_query = normalized_query.strip()

    if not normalized_query:
        raise ValueError("Query cannot be empty.")

    if len(normalized_query) > max_length:
        raise ValueError(f"Query exceeds the maximum length of {max_length} characters.")

    router_text = remove_vietnamese_accents(normalized_query)
    router_text = router_text.lower()
    router_text = re.sub(r"[^\w\s]", " ", router_text)
    router_text = re.sub(r"\s+", " ", router_text)
    router_text = router_text.strip()

    processed_query = {
        "original_query": original_query,
        "normalized_query": normalized_query,
        "router_text": router_text,
    }

    return processed_query