"""aggregation/metric/max.py에 대한 단위 테스트.

MaxAggregation이 올바른 Elasticsearch max 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.metric.max import MaxAggregation


class TestMaxAggregation:
    """MaxAggregation 테스트."""

    def test_max_agg_basic(self):
        """기본 max 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = MaxAggregation.build("price")
        expected = {"max": {"field": "price"}}
        assert result == expected

    def test_max_agg_with_missing(self):
        """missing 옵션이 포함된 max 집계가 올바르게 생성되는지 확인합니다."""
        result = MaxAggregation.build("price", missing=0)
        expected = {"max": {"field": "price", "missing": 0}}
        assert result == expected

    def test_max_agg_without_missing_has_no_key(self):
        """missing을 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = MaxAggregation.build("price")
        assert "missing" not in result["max"]

    def test_max_agg_structure(self):
        """max 집계 결과의 구조가 올바른지 확인합니다."""
        result = MaxAggregation.build("temperature")
        assert "max" in result
        assert "field" in result["max"]
        assert result["max"]["field"] == "temperature"
