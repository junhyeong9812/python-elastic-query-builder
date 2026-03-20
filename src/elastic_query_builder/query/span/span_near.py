"""SpanNear 쿼리 빌더.

여러 span 쿼리의 근접 검색을 수행하는 쿼리를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class SpanNearQuery:
    """근접 검색 쿼리를 생성합니다.

    Elasticsearch span_near 쿼리에 대응합니다.
    여러 span 절 사이의 최대 거리(slop)를 지정하여 근접 검색을 수행합니다.
    in_order 옵션으로 순서 일치 여부를 제어할 수 있습니다.
    """

    @staticmethod
    def build(
        clauses: List[Dict[str, Any]],
        slop: int,
        in_order: Optional[bool] = None,
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """SpanNear 쿼리 딕셔너리를 생성합니다.

        Args:
            clauses: span 쿼리 딕셔너리 목록.
            slop: 절 사이의 최대 허용 거리.
            in_order: 절의 순서를 유지할지 여부 (선택).
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch span_near 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"clauses": clauses, "slop": slop}
        if in_order is not None:
            body["in_order"] = in_order
        if boost is not None:
            body["boost"] = boost
        return {"span_near": body}
