"""SimpleQueryString 쿼리 빌더.

간소화된 구문을 사용하는 simple_query_string 쿼리를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class SimpleQueryStringQuery:
    """SimpleQueryString 쿼리를 생성합니다.

    Elasticsearch simple_query_string 쿼리에 대응합니다.
    간소화된 Lucene 구문으로 검색하며, 구문 오류 시 예외를 발생시키지 않습니다.
    """

    @staticmethod
    def build(
        query: str,
        fields: Optional[List[str]] = None,
        default_operator: Optional[str] = None,
        analyzer: Optional[str] = None,
        flags: Optional[str] = None,
        minimum_should_match: Optional[Any] = None,
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """SimpleQueryString 쿼리 딕셔너리를 생성합니다.

        Args:
            query: 검색 쿼리 문자열.
            fields: 검색할 필드 목록 (선택).
            default_operator: 기본 연산자 (선택). "AND" 또는 "OR".
            analyzer: 사용할 분석기 (선택).
            flags: 활성화할 구문 플래그 (선택). 예: "OR|AND|PREFIX".
            minimum_should_match: 최소 매칭 조건 (선택).
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch simple_query_string 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query}
        if fields is not None:
            body["fields"] = fields
        if default_operator is not None:
            body["default_operator"] = default_operator
        if analyzer is not None:
            body["analyzer"] = analyzer
        if flags is not None:
            body["flags"] = flags
        if minimum_should_match is not None:
            body["minimum_should_match"] = minimum_should_match
        if boost is not None:
            body["boost"] = boost
        return {"simple_query_string": body}
