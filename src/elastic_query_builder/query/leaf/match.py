"""Match 계열 쿼리 빌더.

전문 검색(full-text search)을 위한 match와 match_phrase 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class MatchQuery:
    """전문 검색 쿼리를 생성합니다.

    Elasticsearch match 쿼리에 대응합니다.
    분석기(analyzer)를 통해 텍스트를 분석한 후 검색합니다.
    """

    @staticmethod
    def build(
        field: str,
        query: Any,
        boost: Optional[float] = None,
        fuzziness: Optional[str] = None,
        operator: Optional[str] = None,
        analyzer: Optional[str] = None,
        minimum_should_match: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Match 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            query: 검색 쿼리 텍스트.
            boost: 쿼리 가중치 (선택).
            fuzziness: 퍼지 매칭 수준 (선택). 예: "AUTO", "1", "2".
            operator: 토큰 간 연산자 (선택). "and" 또는 "or".
            analyzer: 사용할 분석기 (선택).
            minimum_should_match: 최소 매칭 비율 (선택). 예: "75%".

        Returns:
            Elasticsearch match 쿼리 딕셔너리.
        """
        match_body: Dict[str, Any] = {"query": query}
        if boost is not None:
            match_body["boost"] = boost
        if fuzziness is not None:
            match_body["fuzziness"] = fuzziness
        if operator is not None:
            match_body["operator"] = operator
        if analyzer is not None:
            match_body["analyzer"] = analyzer
        if minimum_should_match is not None:
            match_body["minimum_should_match"] = minimum_should_match
        return {"match": {field: match_body}}


class MatchPhraseQuery:
    """구문 일치 검색 쿼리를 생성합니다.

    Elasticsearch match_phrase 쿼리에 대응합니다.
    토큰의 순서와 위치까지 고려하여 검색합니다.
    """

    @staticmethod
    def build(
        field: str,
        query: str,
        boost: Optional[float] = None,
        slop: Optional[int] = None,
    ) -> Dict[str, Any]:
        """MatchPhrase 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            query: 검색할 구문.
            boost: 쿼리 가중치 (선택).
            slop: 허용할 토큰 간 거리 (선택).

        Returns:
            Elasticsearch match_phrase 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query}
        if boost is not None:
            body["boost"] = boost
        if slop is not None:
            body["slop"] = slop
        return {"match_phrase": {field: body}}
