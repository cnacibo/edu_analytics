import re

from fastapi import HTTPException


def validate_search_query(q: str) -> str:
    """Валидация поискового запроса"""
    if not q:
        return q

    if len(q) > 200:
        raise HTTPException(
            status_code=400, detail="Поисковый запрос слишком длинный (максимум 200 символов)"
        )

    sql_patterns = [
        r";\s*--",
        r";\s*/\*",
        r"\b(DROP|DELETE|INSERT|UPDATE|ALTER|CREATE|EXEC)\b",
        r"\b(UNION\s+SELECT)\b",
        r"\b(SELECT\s+\*\s+FROM)\b",
    ]

    for pattern in sql_patterns:
        if re.search(pattern, q, re.IGNORECASE):
            raise HTTPException(
                status_code=400, detail="Поисковый запрос содержит недопустимые символы или слова"
            )

    q = q.strip()

    return q
