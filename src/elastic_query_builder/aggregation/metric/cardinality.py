"""Cardinality 집계 빌더.

필드의 고유 값 개수(카디널리티)를 추정하는 metric 집계를 생성합니다.
"""

from typing import Any, Dict, Optional


class CardinalityAggregation:
    """Cardinality metric 집계를 생성합니다.

    Elasticsearch cardinality aggregation에 대응합니다.
    HyperLogLog++ 알고리즘을 사용하여 필드의 고유 값 개수를 추정합니다.
    """

    @staticmethod
    def build(
        field: str,
        precision_threshold: Optional[int] = None,
        missing: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Cardinality 집계 딕셔너리를 생성합니다.

        Args:
            field: 고유 값 개수를 계산할 필드명.
            precision_threshold: 정밀도 임계값 (선택). 높을수록 정확하지만 메모리 사용 증가.
            missing: 필드 값이 없는 문서에 대한 대체 값 (선택).

        Returns:
            Elasticsearch cardinality 집계 딕셔너리.
        """
        body: Dict[str, Any] = {"field": field}
        if precision_threshold is not None:
            body["precision_threshold"] = precision_threshold
        if missing is not None:
            body["missing"] = missing
        return {"cardinality": body}
