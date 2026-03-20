"""DisMax 쿼리 빌더.

여러 쿼리 중 가장 높은 점수를 반환하는 Disjunction Max 쿼리를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class DisMaxQuery:
    """Disjunction Max 쿼리를 생성합니다.

    Elasticsearch dis_max 쿼리에 대응합니다.
    여러 쿼리를 실행하고, 가장 높은 점수를 가진 쿼리의 점수를 문서 점수로 사용합니다.
    tie_breaker를 통해 다른 쿼리의 점수도 일부 반영할 수 있습니다.
    """

    @staticmethod
    def build(
        queries: List[Dict[str, Any]],
        tie_breaker: Optional[float] = None,
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """DisMax 쿼리 딕셔너리를 생성합니다.

        Args:
            queries: 실행할 쿼리 딕셔너리 목록.
            tie_breaker: 최고 점수 외 다른 쿼리 점수의 반영 비율 (선택). 0.0~1.0.
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch dis_max 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"queries": queries}
        if tie_breaker is not None:
            body["tie_breaker"] = tie_breaker
        if boost is not None:
            body["boost"] = boost
        return {"dis_max": body}
