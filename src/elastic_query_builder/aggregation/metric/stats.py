"""Stats 집계 빌더.

숫자 필드의 count, min, max, avg, sum을 한 번에 계산하는 metric 집계를 생성합니다.
"""

from typing import Any, Dict, Optional


class StatsAggregation:
    """Stats metric 집계를 생성합니다.

    Elasticsearch stats aggregation에 대응합니다.
    지정한 숫자 필드의 count, min, max, avg, sum을 한 번에 계산합니다.
    """

    @staticmethod
    def build(field: str, missing: Optional[Any] = None) -> Dict[str, Any]:
        """Stats 집계 딕셔너리를 생성합니다.

        Args:
            field: 통계를 계산할 숫자 필드명.
            missing: 필드 값이 없는 문서에 대한 대체 값 (선택).

        Returns:
            Elasticsearch stats 집계 딕셔너리.
        """
        body: Dict[str, Any] = {"field": field}
        if missing is not None:
            body["missing"] = missing
        return {"stats": body}
