"""SpanTerm 쿼리 빌더.

토큰의 위치 정보를 활용하는 기본 Span 쿼리를 생성합니다.
"""

from typing import Any, Dict


class SpanTermQuery:
    """위치 기반 단일 토큰 검색 쿼리를 생성합니다.

    Elasticsearch span_term 쿼리에 대응합니다.
    span_near 등 다른 span 쿼리의 하위 절(clause)로 사용됩니다.
    """

    @staticmethod
    def build(field: str, value: str) -> Dict[str, Any]:
        """SpanTerm 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            value: 검색할 토큰 값.

        Returns:
            Elasticsearch span_term 쿼리 딕셔너리.
        """
        return {"span_term": {field: value}}
