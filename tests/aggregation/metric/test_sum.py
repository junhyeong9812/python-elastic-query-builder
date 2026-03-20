"""aggregation/metric/sum.py에 대한 단위 테스트.

SumAggregation이 올바른 Elasticsearch sum 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.metric.sum import SumAggregation


class TestSumAggregation:
    """SumAggregation 테스트."""

    def test_sum_agg_basic(self):
        """기본 sum 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = SumAggregation.build("price")
        expected = {"sum": {"field": "price"}}
        assert result == expected

    def test_sum_agg_with_missing(self):
        """missing 옵션이 포함된 sum 집계가 올바르게 생성되는지 확인합니다."""
        result = SumAggregation.build("price", missing=0)
        expected = {"sum": {"field": "price", "missing": 0}}
        assert result == expected

    def test_sum_agg_without_missing_has_no_key(self):
        """missing을 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = SumAggregation.build("price")
        assert "missing" not in result["sum"]

    def test_sum_agg_structure(self):
        """sum 집계 결과의 구조가 올바른지 확인합니다."""
        result = SumAggregation.build("amount")
        assert "sum" in result
        assert "field" in result["sum"]
        assert result["sum"]["field"] == "amount"
