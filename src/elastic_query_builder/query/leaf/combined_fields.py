"""CombinedFields 쿼리 빌더.

여러 필드를 결합하여 검색하는 combined_fields 쿼리를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class CombinedFieldsQuery:
    """CombinedFields 쿼리를 생성합니다.

    Elasticsearch combined_fields 쿼리에 대응합니다.
    여러 필드를 하나의 결합된 필드처럼 취급하여 검색합니다.
    """

    @staticmethod
    def build(
        query: str,
        fields: List[str],
        operator: Optional[str] = None,
        minimum_should_match: Optional[Any] = None,
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """CombinedFields 쿼리 딕셔너리를 생성합니다.

        Args:
            query: 검색 쿼리 텍스트.
            fields: 결합할 필드 목록.
            operator: 토큰 간 연산자 (선택). "and" 또는 "or".
            minimum_should_match: 최소 매칭 조건 (선택).
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch combined_fields 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query, "fields": fields}
        if operator is not None:
            body["operator"] = operator
        if minimum_should_match is not None:
            body["minimum_should_match"] = minimum_should_match
        if boost is not None:
            body["boost"] = boost
        return {"combined_fields": body}
