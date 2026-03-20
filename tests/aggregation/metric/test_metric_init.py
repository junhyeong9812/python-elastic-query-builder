"""aggregation/metric/__init__.py에 대한 단위 테스트.

Metric 집계 패키지에서 모든 클래스를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestMetricAggregationImports:
    """Metric 집계 패키지 import 테스트."""

    def test_import_sum_aggregation(self):
        """metric 패키지에서 SumAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.metric import SumAggregation
        assert SumAggregation is not None

    def test_import_avg_aggregation(self):
        """metric 패키지에서 AvgAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.metric import AvgAggregation
        assert AvgAggregation is not None

    def test_import_min_aggregation(self):
        """metric 패키지에서 MinAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.metric import MinAggregation
        assert MinAggregation is not None

    def test_import_max_aggregation(self):
        """metric 패키지에서 MaxAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.metric import MaxAggregation
        assert MaxAggregation is not None

    def test_import_stats_aggregation(self):
        """metric 패키지에서 StatsAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.metric import StatsAggregation
        assert StatsAggregation is not None

    def test_import_cardinality_aggregation(self):
        """metric 패키지에서 CardinalityAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.metric import CardinalityAggregation
        assert CardinalityAggregation is not None

    def test_import_top_hits_aggregation(self):
        """metric 패키지에서 TopHitsAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.metric import TopHitsAggregation
        assert TopHitsAggregation is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 모든 클래스를 포함하는지 확인합니다."""
        import elastic_query_builder.aggregation.metric as metric_module
        expected_exports = [
            "SumAggregation", "AvgAggregation", "MinAggregation",
            "MaxAggregation", "StatsAggregation",
            "CardinalityAggregation", "TopHitsAggregation",
        ]
        for export in expected_exports:
            assert export in metric_module.__all__, f"{export}이(가) __all__에 없습니다"

    def test_imported_classes_are_functional(self):
        """import한 클래스들이 실제로 동작하는지 확인합니다."""
        from elastic_query_builder.aggregation.metric import (
            SumAggregation, AvgAggregation, MinAggregation,
            MaxAggregation, StatsAggregation,
            CardinalityAggregation, TopHitsAggregation,
        )

        assert "sum" in SumAggregation.build("field")
        assert "avg" in AvgAggregation.build("field")
        assert "min" in MinAggregation.build("field")
        assert "max" in MaxAggregation.build("field")
        assert "stats" in StatsAggregation.build("field")
        assert "cardinality" in CardinalityAggregation.build("field")
        assert "top_hits" in TopHitsAggregation.build()
