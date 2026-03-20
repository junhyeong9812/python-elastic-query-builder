"""aggregation/metric/stats.py에 대한 단위 테스트.

StatsAggregation이 올바른 Elasticsearch stats 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.metric.stats import StatsAggregation


class TestStatsAggregation:
    """StatsAggregation 테스트."""

    def test_stats_agg_basic(self):
        """기본 stats 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = StatsAggregation.build("price")
        expected = {"stats": {"field": "price"}}
        assert result == expected

    def test_stats_agg_with_missing(self):
        """missing 옵션이 포함된 stats 집계가 올바르게 생성되는지 확인합니다."""
        result = StatsAggregation.build("price", missing=0)
        expected = {"stats": {"field": "price", "missing": 0}}
        assert result == expected

    def test_stats_agg_without_missing_has_no_key(self):
        """missing을 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = StatsAggregation.build("price")
        assert "missing" not in result["stats"]

    def test_stats_agg_structure(self):
        """stats 집계 결과의 구조가 올바른지 확인합니다."""
        result = StatsAggregation.build("score")
        assert "stats" in result
        assert "field" in result["stats"]
        assert result["stats"]["field"] == "score"
