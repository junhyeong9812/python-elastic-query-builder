"""aggregation/bucket/filter.py에 대한 단위 테스트.

FilterAggregation과 FiltersAggregation이 올바른 Elasticsearch
filter/filters 집계 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.bucket.filter import (
    FilterAggregation,
    FiltersAggregation,
)


class TestFilterAggregation:
    """FilterAggregation 테스트."""

    def test_filter_agg(self):
        """기본 filter 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = FilterAggregation.build({"term": {"status": {"value": "active"}}})
        expected = {"filter": {"term": {"status": {"value": "active"}}}}
        assert result == expected

    def test_filter_agg_with_bool_query(self):
        """bool 쿼리를 사용한 filter 집계가 올바르게 생성되는지 확인합니다."""
        bool_query = {
            "bool": {
                "must": [
                    {"term": {"status": {"value": "active"}}},
                    {"range": {"age": {"gte": 18}}},
                ]
            }
        }
        result = FilterAggregation.build(bool_query)
        expected = {"filter": bool_query}
        assert result == expected

    def test_filter_agg_structure(self):
        """filter 집계 결과의 구조가 올바른지 확인합니다."""
        result = FilterAggregation.build({"match_all": {}})
        assert "filter" in result
        assert isinstance(result["filter"], dict)


class TestFiltersAggregation:
    """FiltersAggregation 테스트."""

    def test_filters_agg(self):
        """기본 filters 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = FiltersAggregation.build(
            {
                "active": {"term": {"status": {"value": "active"}}},
                "inactive": {"term": {"status": {"value": "inactive"}}},
            }
        )
        expected = {
            "filters": {
                "filters": {
                    "active": {"term": {"status": {"value": "active"}}},
                    "inactive": {"term": {"status": {"value": "inactive"}}},
                }
            }
        }
        assert result == expected

    def test_filters_agg_other_bucket(self):
        """other_bucket 옵션이 포함된 filters 집계가 올바르게 생성되는지 확인합니다."""
        result = FiltersAggregation.build(
            {"active": {"term": {"status": {"value": "active"}}}},
            other_bucket=True,
            other_bucket_key="other",
        )
        expected = {
            "filters": {
                "filters": {
                    "active": {"term": {"status": {"value": "active"}}},
                },
                "other_bucket": True,
                "other_bucket_key": "other",
            }
        }
        assert result == expected

    def test_filters_agg_without_other_bucket_has_no_keys(self):
        """other_bucket 관련 옵션을 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = FiltersAggregation.build(
            {"active": {"term": {"status": {"value": "active"}}}}
        )
        body = result["filters"]
        assert "other_bucket" not in body
        assert "other_bucket_key" not in body

    def test_filters_agg_structure(self):
        """filters 집계 결과의 구조가 올바른지 확인합니다."""
        result = FiltersAggregation.build({"a": {"match_all": {}}})
        assert "filters" in result
        assert "filters" in result["filters"]
        assert isinstance(result["filters"]["filters"], dict)
