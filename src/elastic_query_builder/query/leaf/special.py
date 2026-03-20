"""특수 쿼리 빌더.

MatchAll과 MatchNone 같은 특수 목적 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class MatchAllQuery:
    """모든 문서를 매칭하는 쿼리를 생성합니다.

    Elasticsearch match_all 쿼리에 대응합니다.
    모든 문서를 반환하며, boost로 점수를 조절할 수 있습니다.
    """

    @staticmethod
    def build(boost: Optional[float] = None) -> Dict[str, Any]:
        """MatchAll 쿼리 딕셔너리를 생성합니다.

        Args:
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch match_all 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {}
        if boost is not None:
            body["boost"] = boost
        return {"match_all": body}


class MatchNoneQuery:
    """아무 문서도 매칭하지 않는 쿼리를 생성합니다.

    Elasticsearch match_none 쿼리에 대응합니다.
    항상 빈 결과를 반환합니다.
    """

    @staticmethod
    def build() -> Dict[str, Any]:
        """MatchNone 쿼리 딕셔너리를 생성합니다.

        Returns:
            Elasticsearch match_none 쿼리 딕셔너리.
        """
        return {"match_none": {}}
