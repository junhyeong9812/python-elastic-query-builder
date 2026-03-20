"""aggregation/metric/min.py에 대한 단위 테스트.

MinAggregation이 올바른 Elasticsearch min 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.metric.min import MinAggregation


class TestMinAggregation:
    """MinAggregation 테스트."""

    def test_min_agg_basic(self):
        """기본 min 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = MinAggregation.build("price")
        expected = {"min": {"field": "price"}}
        assert result == expected

    def test_min_agg_with_missing(self):
        """missing 옵션이 포함된 min 집계가 올바르게 생성되는지 확인합니다."""
        result = MinAggregation.build("price", missing=0)
        expected = {"min": {"field": "price", "missing": 0}}
        assert result == expected

    def test_min_agg_without_missing_has_no_key(self):
        """missing을 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = MinAggregation.build("price")
        assert "missing" not in result["min"]

    def test_min_agg_structure(self):
        """min 집계 결과의 구조가 올바른지 확인합니다."""
        result = MinAggregation.build("temperature")
        assert "min" in result
        assert "field" in result["min"]
        assert result["min"]["field"] == "temperature"
