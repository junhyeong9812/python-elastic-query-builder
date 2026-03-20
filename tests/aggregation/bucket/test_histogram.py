"""aggregation/bucket/histogram.py에 대한 단위 테스트.

HistogramAggregation이 올바른 Elasticsearch histogram 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.bucket.histogram import HistogramAggregation


class TestHistogramAggregation:
    """HistogramAggregation 테스트."""

    def test_histogram_basic(self):
        """기본 histogram 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = HistogramAggregation.build("price", interval=100)
        expected = {"histogram": {"field": "price", "interval": 100}}
        assert result == expected

    def test_histogram_with_min_doc_count(self):
        """min_doc_count 옵션이 포함된 histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = HistogramAggregation.build("price", interval=100, min_doc_count=1)
        expected = {
            "histogram": {
                "field": "price",
                "interval": 100,
                "min_doc_count": 1,
            }
        }
        assert result == expected

    def test_histogram_with_extended_bounds(self):
        """extended_bounds 옵션이 포함된 histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = HistogramAggregation.build(
            "price",
            interval=100,
            extended_bounds={"min": 0, "max": 1000},
        )
        expected = {
            "histogram": {
                "field": "price",
                "interval": 100,
                "extended_bounds": {"min": 0, "max": 1000},
            }
        }
        assert result == expected

    def test_histogram_without_optional_has_no_keys(self):
        """선택 옵션을 지정하지 않으면 결과에 해당 키가 없는지 확인합니다."""
        result = HistogramAggregation.build("price", interval=50)
        body = result["histogram"]
        assert "min_doc_count" not in body
        assert "extended_bounds" not in body

    def test_histogram_structure(self):
        """histogram 집계 결과의 구조가 올바른지 확인합니다."""
        result = HistogramAggregation.build("price", interval=100)
        assert "histogram" in result
        assert "field" in result["histogram"]
        assert "interval" in result["histogram"]
        assert result["histogram"]["field"] == "price"
        assert result["histogram"]["interval"] == 100

    def test_histogram_float_interval(self):
        """실수 interval을 사용한 histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = HistogramAggregation.build("score", interval=0.5)
        expected = {"histogram": {"field": "score", "interval": 0.5}}
        assert result == expected
