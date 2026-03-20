"""aggregation/bucket/date_histogram.py에 대한 단위 테스트.

DateHistogramAggregation이 올바른 Elasticsearch date_histogram 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.bucket.date_histogram import DateHistogramAggregation


class TestDateHistogramAggregation:
    """DateHistogramAggregation 테스트."""

    def test_date_histogram_calendar_interval(self):
        """calendar_interval을 사용한 date_histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = DateHistogramAggregation.build("date", calendar_interval="1M")
        expected = {
            "date_histogram": {
                "field": "date",
                "calendar_interval": "1M",
            }
        }
        assert result == expected

    def test_date_histogram_fixed_interval(self):
        """fixed_interval을 사용한 date_histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = DateHistogramAggregation.build("date", fixed_interval="30d")
        expected = {
            "date_histogram": {
                "field": "date",
                "fixed_interval": "30d",
            }
        }
        assert result == expected

    def test_date_histogram_with_format(self):
        """format 옵션이 포함된 date_histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = DateHistogramAggregation.build(
            "date", calendar_interval="1M", format="yyyy-MM-dd"
        )
        expected = {
            "date_histogram": {
                "field": "date",
                "calendar_interval": "1M",
                "format": "yyyy-MM-dd",
            }
        }
        assert result == expected

    def test_date_histogram_with_time_zone(self):
        """time_zone 옵션이 포함된 date_histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = DateHistogramAggregation.build(
            "date", calendar_interval="1d", time_zone="Asia/Seoul"
        )
        expected = {
            "date_histogram": {
                "field": "date",
                "calendar_interval": "1d",
                "time_zone": "Asia/Seoul",
            }
        }
        assert result == expected

    def test_date_histogram_with_min_doc_count(self):
        """min_doc_count 옵션이 포함된 date_histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = DateHistogramAggregation.build(
            "date", calendar_interval="1M", min_doc_count=0
        )
        expected = {
            "date_histogram": {
                "field": "date",
                "calendar_interval": "1M",
                "min_doc_count": 0,
            }
        }
        assert result == expected

    def test_date_histogram_with_extended_bounds(self):
        """extended_bounds 옵션이 포함된 date_histogram 집계가 올바르게 생성되는지 확인합니다."""
        result = DateHistogramAggregation.build(
            "date",
            calendar_interval="1M",
            extended_bounds={"min": "2024-01-01", "max": "2024-12-31"},
        )
        expected = {
            "date_histogram": {
                "field": "date",
                "calendar_interval": "1M",
                "extended_bounds": {"min": "2024-01-01", "max": "2024-12-31"},
            }
        }
        assert result == expected

    def test_date_histogram_without_optional_has_no_keys(self):
        """선택 옵션을 지정하지 않으면 결과에 해당 키가 없는지 확인합니다."""
        result = DateHistogramAggregation.build("date")
        body = result["date_histogram"]
        assert "calendar_interval" not in body
        assert "fixed_interval" not in body
        assert "format" not in body
        assert "time_zone" not in body
        assert "min_doc_count" not in body
        assert "extended_bounds" not in body

    def test_date_histogram_structure(self):
        """date_histogram 집계 결과의 구조가 올바른지 확인합니다."""
        result = DateHistogramAggregation.build("date", calendar_interval="1M")
        assert "date_histogram" in result
        assert "field" in result["date_histogram"]
        assert result["date_histogram"]["field"] == "date"
