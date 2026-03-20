"""DateHistogram 집계 빌더.

날짜 필드를 일정 간격으로 분할하여 집계하는 bucket 집계를 생성합니다.
"""

from typing import Any, Dict, Optional


class DateHistogramAggregation:
    """DateHistogram bucket 집계를 생성합니다.

    Elasticsearch date_histogram aggregation에 대응합니다.
    날짜 필드를 calendar_interval 또는 fixed_interval로 분할하여
    시간대별 문서 분포를 집계합니다.
    """

    @staticmethod
    def build(
        field: str,
        calendar_interval: Optional[str] = None,
        fixed_interval: Optional[str] = None,
        format: Optional[str] = None,
        time_zone: Optional[str] = None,
        min_doc_count: Optional[int] = None,
        extended_bounds: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """DateHistogram 집계 딕셔너리를 생성합니다.

        Args:
            field: 집계할 날짜 필드명.
            calendar_interval: 달력 기반 간격 (선택). 예: "1M", "1y".
            fixed_interval: 고정 간격 (선택). 예: "30d", "1h".
            format: 날짜 출력 형식 (선택). 예: "yyyy-MM-dd".
            time_zone: 시간대 (선택). 예: "Asia/Seoul".
            min_doc_count: 최소 문서 수 (선택).
            extended_bounds: 확장 범위 (선택). 예: {"min": "2024-01-01", "max": "2024-12-31"}.

        Returns:
            Elasticsearch date_histogram 집계 딕셔너리.
        """
        body: Dict[str, Any] = {"field": field}
        if calendar_interval is not None:
            body["calendar_interval"] = calendar_interval
        if fixed_interval is not None:
            body["fixed_interval"] = fixed_interval
        if format is not None:
            body["format"] = format
        if time_zone is not None:
            body["time_zone"] = time_zone
        if min_doc_count is not None:
            body["min_doc_count"] = min_doc_count
        if extended_bounds is not None:
            body["extended_bounds"] = extended_bounds
        return {"date_histogram": body}
