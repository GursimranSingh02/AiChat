from typing import Tuple


def validate_query(query: str) -> Tuple[bool, str]:
    cleaned = (query or "").strip()

    if not cleaned:
        return False, "Query is required"

    if len(cleaned) > 5000:
        return False, "Query is too long"

    return True, "Valid query"
