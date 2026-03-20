"""AggregationBuilder — 복수 Aggregation 조합 빌더.

여러 개의 집계를 하나로 묶어 최종 Elasticsearch aggs 딕셔너리를 생성합니다.
개별 Aggregation 클래스를 내부에서 활용하여 편의 메서드를 제공하며,
메서드 체이닝을 지원합니다.
"""

from typing import Any, Dict, Optional
from elastic_query_builder.aggregation.bucket.terms import TermsAggregation
from elastic_query_builder.aggregation.bucket.date_histogram import DateHistogramAggregation
from elastic_query_builder.aggregation.metric.cardinality import CardinalityAggregation
from elastic_query_builder.aggregation.metric.stats import StatsAggregation
from elastic_query_builder.aggregation.bucket.nested import NestedAggregation


class AggregationBuilder:
    """복수의 Aggregation을 조합하는 빌더.

    add_aggregation()으로 직접 집계를 추가하거나,
    add_terms(), add_date_histogram() 등의 편의 메서드를 사용하여
    간편하게 집계를 구성할 수 있습니다.
    모든 메서드는 self를 반환하여 메서드 체이닝을 지원합니다.
    """

    def __init__(self):
        self._aggregations: Dict[str, Any] = {}

    def add_aggregation(
        self, name: str, agg_body: Dict[str, Any], sub_aggs: Optional[Dict[str, Any]] = None
    ) -> 'AggregationBuilder':
        """이름과 집계 본문을 직접 추가합니다.

        Args:
            name: 집계 이름.
            agg_body: 집계 본문 딕셔너리. 예: {"terms": {"field": "status"}}.
            sub_aggs: 하위 집계 딕셔너리 (선택).

        Returns:
            메서드 체이닝을 위한 self.
        """
        entry: Dict[str, Any] = dict(agg_body)
        if sub_aggs is not None:
            entry["aggs"] = sub_aggs
        self._aggregations[name] = entry
        return self

    def add_terms(
        self, name: str, field: str, size: Optional[int] = None,
        order: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> 'AggregationBuilder':
        """Terms 집계를 추가합니다.

        Args:
            name: 집계 이름.
            field: 집계할 필드명.
            size: 반환할 버킷 수 (선택).
            order: 버킷 정렬 기준 (선택).
            **kwargs: TermsAggregation.build()에 전달할 추가 옵션.

        Returns:
            메서드 체이닝을 위한 self.
        """
        agg = TermsAggregation.build(field, size=size, order=order, **kwargs)
        return self.add_aggregation(name, agg)

    def add_date_histogram(
        self, name: str, field: str,
        calendar_interval: Optional[str] = None,
        fixed_interval: Optional[str] = None,
        format: Optional[str] = None,
        time_zone: Optional[str] = None,
        min_doc_count: Optional[int] = None,
        extended_bounds: Optional[Dict[str, Any]] = None,
    ) -> 'AggregationBuilder':
        """DateHistogram 집계를 추가합니다.

        Args:
            name: 집계 이름.
            field: 집계할 날짜 필드명.
            calendar_interval: 달력 기반 간격 (선택).
            fixed_interval: 고정 간격 (선택).
            format: 날짜 출력 형식 (선택).
            time_zone: 시간대 (선택).
            min_doc_count: 최소 문서 수 (선택).
            extended_bounds: 확장 범위 (선택).

        Returns:
            메서드 체이닝을 위한 self.
        """
        agg = DateHistogramAggregation.build(
            field, calendar_interval=calendar_interval, fixed_interval=fixed_interval,
            format=format, time_zone=time_zone, min_doc_count=min_doc_count,
            extended_bounds=extended_bounds,
        )
        return self.add_aggregation(name, agg)

    def add_cardinality(
        self, name: str, field: str, precision_threshold: Optional[int] = None
    ) -> 'AggregationBuilder':
        """Cardinality 집계를 추가합니다.

        Args:
            name: 집계 이름.
            field: 고유 값 개수를 계산할 필드명.
            precision_threshold: 정밀도 임계값 (선택).

        Returns:
            메서드 체이닝을 위한 self.
        """
        agg = CardinalityAggregation.build(field, precision_threshold=precision_threshold)
        return self.add_aggregation(name, agg)

    def add_stats(
        self, name: str, field: str, missing: Optional[Any] = None
    ) -> 'AggregationBuilder':
        """Stats 집계를 추가합니다.

        Args:
            name: 집계 이름.
            field: 통계를 계산할 필드명.
            missing: 필드 값이 없는 문서에 대한 대체 값 (선택).

        Returns:
            메서드 체이닝을 위한 self.
        """
        agg = StatsAggregation.build(field, missing=missing)
        return self.add_aggregation(name, agg)

    def add_nested_aggregation(
        self, name: str, path: str, sub_aggs: Dict[str, Any]
    ) -> 'AggregationBuilder':
        """Nested 집계를 추가합니다.

        Args:
            name: 집계 이름.
            path: nested 필드 경로.
            sub_aggs: 하위 집계 딕셔너리.

        Returns:
            메서드 체이닝을 위한 self.
        """
        agg = NestedAggregation.build(path)
        return self.add_aggregation(name, agg, sub_aggs=sub_aggs)

    def is_empty(self) -> bool:
        """빌더에 추가된 집계가 없는지 확인합니다.

        Returns:
            집계가 없으면 True, 있으면 False.
        """
        return len(self._aggregations) == 0

    def build(self) -> Dict[str, Any]:
        """최종 집계 딕셔너리를 생성합니다.

        Returns:
            집계 이름을 키로, 집계 본문을 값으로 하는 딕셔너리.
        """
        return dict(self._aggregations)
