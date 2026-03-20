"""Histogram 집계 빌더.

숫자 필드를 일정 간격으로 분할하여 집계하는 bucket 집계를 생성합니다.
"""

from typing import Any, Dict, Optional


class HistogramAggregation:
    """Histogram bucket 집계를 생성합니다.

    Elasticsearch histogram aggregation에 대응합니다.
    숫자 필드를 지정한 interval로 분할하여 구간별 문서 분포를 집계합니다.
    """

    @staticmethod
    def build(
        field: str,
        interval: float,
        min_doc_count: Optional[int] = None,
        extended_bounds: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Histogram 집계 딕셔너리를 생성합니다.

        Args:
            field: 집계할 숫자 필드명.
            interval: 버킷 간격.
            min_doc_count: 최소 문서 수 (선택).
            extended_bounds: 확장 범위 (선택). 예: {"min": 0, "max": 1000}.

        Returns:
            Elasticsearch histogram 집계 딕셔너리.
        """
        body: Dict[str, Any] = {"field": field, "interval": interval}
        if min_doc_count is not None:
            body["min_doc_count"] = min_doc_count
        if extended_bounds is not None:
            body["extended_bounds"] = extended_bounds
        return {"histogram": body}
