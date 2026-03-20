"""aggregation/__init__.py에 대한 단위 테스트.

Aggregation 패키지에서 모든 클래스를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestAggregationPackageImports:
    """Aggregation 패키지 import 테스트."""

    def test_import_aggregation_builder(self):
        """aggregation 패키지에서 AggregationBuilder를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import AggregationBuilder
        assert AggregationBuilder is not None

    def test_import_terms_aggregation(self):
        """aggregation 패키지에서 TermsAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import TermsAggregation
        assert TermsAggregation is not None

    def test_import_date_histogram_aggregation(self):
        """aggregation 패키지에서 DateHistogramAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import DateHistogramAggregation
        assert DateHistogramAggregation is not None

    def test_import_histogram_aggregation(self):
        """aggregation 패키지에서 HistogramAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import HistogramAggregation
        assert HistogramAggregation is not None

    def test_import_range_aggregation(self):
        """aggregation 패키지에서 RangeAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import RangeAggregation
        assert RangeAggregation is not None

    def test_import_filter_aggregation(self):
        """aggregation 패키지에서 FilterAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import FilterAggregation
        assert FilterAggregation is not None

    def test_import_filters_aggregation(self):
        """aggregation 패키지에서 FiltersAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import FiltersAggregation
        assert FiltersAggregation is not None

    def test_import_nested_aggregation(self):
        """aggregation 패키지에서 NestedAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import NestedAggregation
        assert NestedAggregation is not None

    def test_import_sum_aggregation(self):
        """aggregation 패키지에서 SumAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import SumAggregation
        assert SumAggregation is not None

    def test_import_avg_aggregation(self):
        """aggregation 패키지에서 AvgAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import AvgAggregation
        assert AvgAggregation is not None

    def test_import_min_aggregation(self):
        """aggregation 패키지에서 MinAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import MinAggregation
        assert MinAggregation is not None

    def test_import_max_aggregation(self):
        """aggregation 패키지에서 MaxAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import MaxAggregation
        assert MaxAggregation is not None

    def test_import_stats_aggregation(self):
        """aggregation 패키지에서 StatsAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import StatsAggregation
        assert StatsAggregation is not None

    def test_import_cardinality_aggregation(self):
        """aggregation 패키지에서 CardinalityAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import CardinalityAggregation
        assert CardinalityAggregation is not None

    def test_import_top_hits_aggregation(self):
        """aggregation 패키지에서 TopHitsAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation import TopHitsAggregation
        assert TopHitsAggregation is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 모든 클래스를 포함하는지 확인합니다."""
        import elastic_query_builder.aggregation as agg_module
        expected_exports = [
            "AggregationBuilder",
            "TermsAggregation", "DateHistogramAggregation", "HistogramAggregation",
            "RangeAggregation", "FilterAggregation", "FiltersAggregation", "NestedAggregation",
            "SumAggregation", "AvgAggregation", "MinAggregation", "MaxAggregation",
            "StatsAggregation", "CardinalityAggregation", "TopHitsAggregation",
        ]
        for export in expected_exports:
            assert export in agg_module.__all__, f"{export}이(가) __all__에 없습니다"

    def test_imported_classes_are_functional(self):
        """import한 클래스들이 실제로 동작하는지 확인합니다."""
        from elastic_query_builder.aggregation import (
            AggregationBuilder, TermsAggregation, CardinalityAggregation,
        )
        builder = AggregationBuilder()
        assert builder.is_empty() is True
        assert "terms" in TermsAggregation.build("field")
        assert "cardinality" in CardinalityAggregation.build("field")
