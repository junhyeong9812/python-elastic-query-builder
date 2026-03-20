"""Prefix 쿼리 빌더.

접두사 기반 검색 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class PrefixQuery:
    """접두사 매칭 쿼리를 생성합니다.

    Elasticsearch prefix 쿼리에 대응합니다.
    지정된 접두사로 시작하는 용어를 검색합니다.
    """

    @staticmethod
    def build(
        field: str,
        value: str,
        boost: Optional[float] = None,
        case_insensitive: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Prefix 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            value: 접두사 문자열.
            boost: 쿼리 가중치 (선택).
            case_insensitive: 대소문자 무시 여부 (선택).

        Returns:
            Elasticsearch prefix 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"value": value}
        if boost is not None:
            body["boost"] = boost
        if case_insensitive is not None:
            body["case_insensitive"] = case_insensitive
        return {"prefix": {field: body}}
