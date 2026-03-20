"""more_like_this 쿼리 빌더.

Elasticsearch의 more_like_this 쿼리를 생성합니다.
주어진 텍스트나 문서와 유사한 문서를 검색합니다.
"""

from typing import Any, Dict, List, Optional


class MoreLikeThisQuery:
    """more_like_this 쿼리 빌더."""

    @staticmethod
    def build(
        fields: List[str],
        like: Any,
        min_term_freq: Optional[int] = None,
        min_doc_freq: Optional[int] = None,
        max_query_terms: Optional[int] = None,
        minimum_should_match: Optional[Any] = None,
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """more_like_this 쿼리 딕셔너리를 생성합니다.

        Args:
            fields: 검색할 필드 목록.
            like: 유사 문서를 찾기 위한 텍스트 또는 문서.
            min_term_freq: 최소 용어 빈도.
            min_doc_freq: 최소 문서 빈도.
            max_query_terms: 최대 쿼리 용어 수.
            minimum_should_match: 최소 일치 조건.
            boost: 부스트 값.

        Returns:
            more_like_this 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"fields": fields, "like": like}
        if min_term_freq is not None:
            body["min_term_freq"] = min_term_freq
        if min_doc_freq is not None:
            body["min_doc_freq"] = min_doc_freq
        if max_query_terms is not None:
            body["max_query_terms"] = max_query_terms
        if minimum_should_match is not None:
            body["minimum_should_match"] = minimum_should_match
        if boost is not None:
            body["boost"] = boost
        return {"more_like_this": body}
