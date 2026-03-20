"""Metric 집계 패키지.

Elasticsearch의 Metric Aggregation 빌더들을 제공합니다.
Metric 집계는 문서의 숫자 필드에서 통계 값을 계산하는 집계입니다.
"""

from elastic_query_builder.aggregation.metric.sum import SumAggregation
from elastic_query_builder.aggregation.metric.avg import AvgAggregation
from elastic_query_builder.aggregation.metric.min import MinAggregation
from elastic_query_builder.aggregation.metric.max import MaxAggregation
from elastic_query_builder.aggregation.metric.stats import StatsAggregation
from elastic_query_builder.aggregation.metric.cardinality import CardinalityAggregation
from elastic_query_builder.aggregation.metric.top_hits import TopHitsAggregation

__all__ = [
    "SumAggregation",
    "AvgAggregation",
    "MinAggregation",
    "MaxAggregation",
    "StatsAggregation",
    "CardinalityAggregation",
    "TopHitsAggregation",
]
