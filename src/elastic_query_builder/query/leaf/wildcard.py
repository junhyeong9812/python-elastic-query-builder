"""Wildcard 쿼리 빌더.

와일드카드 패턴을 사용한 검색 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class WildcardQuery:
    """와일드카드 패턴 매칭 쿼리를 생성합니다.

    Elasticsearch wildcard 쿼리에 대응합니다.
    '*'는 0개 이상의 문자, '?'는 정확히 1개의 문자와 일치합니다.
    """

    @staticmethod
    def build(
        field: str,
        value: str,
        boost: Optional[float] = None,
        case_insensitive: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Wildcard 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            value: 와일드카드 패턴 문자열.
            boost: 쿼리 가중치 (선택).
            case_insensitive: 대소문자 무시 여부 (선택).

        Returns:
            Elasticsearch wildcard 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"value": value}
        if boost is not None:
            body["boost"] = boost
        if case_insensitive is not None:
            body["case_insensitive"] = case_insensitive
        return {"wildcard": {field: body}}
