"""aggregation/metric/avg.py에 대한 단위 테스트.

AvgAggregation이 올바른 Elasticsearch avg 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.metric.avg import AvgAggregation


class TestAvgAggregation:
    """AvgAggregation 테스트."""

    def test_avg_agg_basic(self):
        """기본 avg 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = AvgAggregation.build("score")
        expected = {"avg": {"field": "score"}}
        assert result == expected

    def test_avg_agg_with_missing(self):
        """missing 옵션이 포함된 avg 집계가 올바르게 생성되는지 확인합니다."""
        result = AvgAggregation.build("score", missing=0)
        expected = {"avg": {"field": "score", "missing": 0}}
        assert result == expected

    def test_avg_agg_without_missing_has_no_key(self):
        """missing을 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = AvgAggregation.build("score")
        assert "missing" not in result["avg"]

    def test_avg_agg_structure(self):
        """avg 집계 결과의 구조가 올바른지 확인합니다."""
        result = AvgAggregation.build("rating")
        assert "avg" in result
        assert "field" in result["avg"]
        assert result["avg"]["field"] == "rating"
