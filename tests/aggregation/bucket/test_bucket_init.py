"""aggregation/bucket/__init__.py에 대한 단위 테스트.

Bucket 집계 패키지에서 모든 클래스를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestBucketAggregationImports:
    """Bucket 집계 패키지 import 테스트."""

    def test_import_terms_aggregation(self):
        """bucket 패키지에서 TermsAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.bucket import TermsAggregation
        assert TermsAggregation is not None

    def test_import_date_histogram_aggregation(self):
        """bucket 패키지에서 DateHistogramAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.bucket import DateHistogramAggregation
        assert DateHistogramAggregation is not None

    def test_import_histogram_aggregation(self):
        """bucket 패키지에서 HistogramAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.bucket import HistogramAggregation
        assert HistogramAggregation is not None

    def test_import_range_aggregation(self):
        """bucket 패키지에서 RangeAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.bucket import RangeAggregation
        assert RangeAggregation is not None

    def test_import_filter_aggregation(self):
        """bucket 패키지에서 FilterAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.bucket import FilterAggregation
        assert FilterAggregation is not None

    def test_import_filters_aggregation(self):
        """bucket 패키지에서 FiltersAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.bucket import FiltersAggregation
        assert FiltersAggregation is not None

    def test_import_nested_aggregation(self):
        """bucket 패키지에서 NestedAggregation을 import할 수 있는지 확인합니다."""
        from elastic_query_builder.aggregation.bucket import NestedAggregation
        assert NestedAggregation is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 모든 클래스를 포함하는지 확인합니다."""
        import elastic_query_builder.aggregation.bucket as bucket_module
        expected_exports = [
            "TermsAggregation", "DateHistogramAggregation", "HistogramAggregation",
            "RangeAggregation", "FilterAggregation", "FiltersAggregation",
            "NestedAggregation",
        ]
        for export in expected_exports:
            assert export in bucket_module.__all__, f"{export}이(가) __all__에 없습니다"

    def test_imported_classes_are_functional(self):
        """import한 클래스들이 실제로 동작하는지 확인합니다."""
        from elastic_query_builder.aggregation.bucket import (
            TermsAggregation, DateHistogramAggregation, HistogramAggregation,
            RangeAggregation, FilterAggregation, FiltersAggregation,
            NestedAggregation,
        )

        assert "terms" in TermsAggregation.build("field")
        assert "date_histogram" in DateHistogramAggregation.build("date", calendar_interval="1M")
        assert "histogram" in HistogramAggregation.build("price", interval=100)
        assert "range" in RangeAggregation.build("price", ranges=[{"to": 100}])
        assert "filter" in FilterAggregation.build({"match_all": {}})
        assert "filters" in FiltersAggregation.build({"a": {"match_all": {}}})
        assert "nested" in NestedAggregation.build("items")
