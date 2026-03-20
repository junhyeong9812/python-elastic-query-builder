"""MatchPhrasePrefix 쿼리 빌더.

구문 접두사 매칭을 위한 match_phrase_prefix 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class MatchPhrasePrefixQuery:
    """구문 접두사 검색 쿼리를 생성합니다.

    Elasticsearch match_phrase_prefix 쿼리에 대응합니다.
    마지막 토큰을 접두사로 사용하여 구문 검색을 수행합니다.
    """

    @staticmethod
    def build(
        field: str,
        query: str,
        max_expansions: Optional[int] = None,
        boost: Optional[float] = None,
        slop: Optional[int] = None,
        analyzer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """MatchPhrasePrefix 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            query: 검색할 구문.
            max_expansions: 마지막 토큰의 최대 확장 수 (선택).
            boost: 쿼리 가중치 (선택).
            slop: 허용할 토큰 간 거리 (선택).
            analyzer: 사용할 분석기 (선택).

        Returns:
            Elasticsearch match_phrase_prefix 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query}
        if max_expansions is not None:
            body["max_expansions"] = max_expansions
        if boost is not None:
            body["boost"] = boost
        if slop is not None:
            body["slop"] = slop
        if analyzer is not None:
            body["analyzer"] = analyzer
        return {"match_phrase_prefix": {field: body}}
