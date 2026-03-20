"""MatchBoolPrefix 쿼리 빌더.

Bool 접두사 매칭을 위한 match_bool_prefix 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class MatchBoolPrefixQuery:
    """Bool 접두사 검색 쿼리를 생성합니다.

    Elasticsearch match_bool_prefix 쿼리에 대응합니다.
    마지막 토큰은 접두사로, 나머지 토큰은 term으로 검색합니다.
    """

    @staticmethod
    def build(
        field: str,
        query: str,
        boost: Optional[float] = None,
        fuzziness: Optional[Any] = None,
        operator: Optional[str] = None,
        minimum_should_match: Optional[Any] = None,
        analyzer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """MatchBoolPrefix 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            query: 검색 쿼리 텍스트.
            boost: 쿼리 가중치 (선택).
            fuzziness: 퍼지 매칭 수준 (선택). 예: "AUTO", "1", "2".
            operator: 토큰 간 연산자 (선택). "and" 또는 "or".
            minimum_should_match: 최소 매칭 비율 (선택). 예: "75%".
            analyzer: 사용할 분석기 (선택).

        Returns:
            Elasticsearch match_bool_prefix 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query}
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
        return {"match_bool_prefix": {field: body}}
