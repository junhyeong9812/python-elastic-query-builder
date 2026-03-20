"""MultiMatch 쿼리 빌더.

여러 필드에 걸쳐 전문 검색(full-text search)을 수행하는 multi_match 쿼리를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class MultiMatchQuery:
    """여러 필드에 대한 전문 검색 쿼리를 생성합니다.

    Elasticsearch multi_match 쿼리에 대응합니다.
    여러 필드에서 동시에 텍스트를 검색할 때 사용합니다.
    """

    @staticmethod
    def build(
        fields: List[str],
        query: str,
        type: Optional[str] = None,
        tie_breaker: Optional[float] = None,
        boost: Optional[float] = None,
        fuzziness: Optional[Any] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[Any] = None,
        analyzer: Optional[str] = None,
        max_expansions: Optional[int] = None,
        prefix_length: Optional[int] = None,
        zero_terms_query: Optional[str] = None,
    ) -> Dict[str, Any]:
        """MultiMatch 쿼리 딕셔너리를 생성합니다.

        Args:
            fields: 검색할 필드 목록. 부스트 표기법 지원 (예: "title^2").
            query: 검색 쿼리 텍스트.
            type: 매칭 타입 (선택). 예: "best_fields", "most_fields".
            tie_breaker: 타이 브레이커 값 (선택). 0.0~1.0.
            boost: 쿼리 가중치 (선택).
            fuzziness: 퍼지 매칭 수준 (선택). 예: "AUTO", "1", "2".
            operator: 토큰 간 연산자 (선택). "and" 또는 "or".
            minimum_should_match: 최소 매칭 비율 (선택). 예: "75%".
            analyzer: 사용할 분석기 (선택).
            max_expansions: 최대 확장 수 (선택).
            prefix_length: 접두사 길이 (선택).
            zero_terms_query: 모든 토큰이 제거됐을 때의 동작 (선택).

        Returns:
            Elasticsearch multi_match 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query, "fields": fields}
        if type is not None:
            body["type"] = type
        if tie_breaker is not None:
            body["tie_breaker"] = tie_breaker
        if boost is not None:
            body["boost"] = boost
        if fuzziness is not None:
            body["fuzziness"] = fuzziness
        if operator is not None:
            body["operator"] = operator
        if minimum_should_match is not None:
            body["minimum_should_match"] = minimum_should_match
        if analyzer is not None:
            body["analyzer"] = analyzer
        if max_expansions is not None:
            body["max_expansions"] = max_expansions
        if prefix_length is not None:
            body["prefix_length"] = prefix_length
        if zero_terms_query is not None:
            body["zero_terms_query"] = zero_terms_query
        return {"multi_match": body}
