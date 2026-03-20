"""QueryString 쿼리 빌더.

Lucene 쿼리 구문을 사용하는 query_string 쿼리를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class QueryStringQuery:
    """QueryString 쿼리를 생성합니다.

    Elasticsearch query_string 쿼리에 대응합니다.
    Lucene 쿼리 파서 구문을 사용하여 복잡한 검색을 수행합니다.
    """

    @staticmethod
    def build(
        query: str,
        fields: Optional[List[str]] = None,
        default_field: Optional[str] = None,
        default_operator: Optional[str] = None,
        analyzer: Optional[str] = None,
        allow_leading_wildcard: Optional[bool] = None,
        fuzziness: Optional[Any] = None,
        boost: Optional[float] = None,
        minimum_should_match: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """QueryString 쿼리 딕셔너리를 생성합니다.

        Args:
            query: Lucene 쿼리 구문 문자열.
            fields: 검색할 필드 목록 (선택).
            default_field: 기본 검색 필드 (선택).
            default_operator: 기본 연산자 (선택). "AND" 또는 "OR".
            analyzer: 사용할 분석기 (선택).
            allow_leading_wildcard: 선행 와일드카드 허용 여부 (선택).
            fuzziness: 퍼지 매칭 수준 (선택).
            boost: 쿼리 가중치 (선택).
            minimum_should_match: 최소 매칭 조건 (선택).

        Returns:
            Elasticsearch query_string 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query}
        if fields is not None:
            body["fields"] = fields
        if default_field is not None:
            body["default_field"] = default_field
        if default_operator is not None:
            body["default_operator"] = default_operator
        if analyzer is not None:
            body["analyzer"] = analyzer
        if allow_leading_wildcard is not None:
            body["allow_leading_wildcard"] = allow_leading_wildcard
        if fuzziness is not None:
            body["fuzziness"] = fuzziness
        if boost is not None:
            body["boost"] = boost
        if minimum_should_match is not None:
            body["minimum_should_match"] = minimum_should_match
        return {"query_string": body}
