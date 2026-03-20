"""TermsSet 쿼리 빌더.

지정된 필드에서 최소 매칭 조건을 만족하는 terms_set 쿼리를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class TermsSetQuery:
    """TermsSet 쿼리를 생성합니다.

    Elasticsearch terms_set 쿼리에 대응합니다.
    지정된 필드에서 최소 매칭 조건과 함께 여러 값을 검색합니다.
    """

    @staticmethod
    def build(
        field: str,
        terms: List[Any],
        minimum_should_match_field: Optional[str] = None,
        minimum_should_match_script: Optional[Dict[str, Any]] = None,
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """TermsSet 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            terms: 검색할 값 목록.
            minimum_should_match_field: 최소 매칭 수를 지정하는 필드명 (선택).
            minimum_should_match_script: 최소 매칭 수를 계산하는 스크립트 (선택).
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch terms_set 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"terms": terms}
        if minimum_should_match_field is not None:
            body["minimum_should_match_field"] = minimum_should_match_field
        if minimum_should_match_script is not None:
            body["minimum_should_match_script"] = minimum_should_match_script
        if boost is not None:
            body["boost"] = boost
        return {"terms_set": {field: body}}
