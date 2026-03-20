"""query/leaf/range.py에 대한 단위 테스트.

RangeQuery가 올바른 Elasticsearch 범위 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.range import RangeQuery


class TestRangeQuery:
    """RangeQuery 테스트."""

    def test_range_query_gte_lte(self):
        """gte와 lte를 사용한 범위 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RangeQuery.build("price", gte=100, lte=500)
        expected = {"range": {"price": {"gte": 100, "lte": 500}}}
        assert result == expected

    def test_range_query_gt_lt(self):
        """gt와 lt를 사용한 범위 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RangeQuery.build("price", gt=100, lt=500)
        expected = {"range": {"price": {"gt": 100, "lt": 500}}}
        assert result == expected

    def test_range_query_single_bound_gte(self):
        """하한만 지정한 범위 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RangeQuery.build("age", gte=18)
        expected = {"range": {"age": {"gte": 18}}}
        assert result == expected

    def test_range_query_single_bound_lte(self):
        """상한만 지정한 범위 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RangeQuery.build("age", lte=65)
        expected = {"range": {"age": {"lte": 65}}}
        assert result == expected

    def test_range_query_with_format(self):
        """날짜 포맷이 포함된 범위 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RangeQuery.build("date", gte="2024-01-01", format="yyyy-MM-dd")
        expected = {
            "range": {
                "date": {
                    "gte": "2024-01-01",
                    "format": "yyyy-MM-dd",
                }
            }
        }
        assert result == expected

    def test_range_query_with_boost(self):
        """boost가 포함된 범위 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RangeQuery.build("price", gte=100, lte=500, boost=1.5)
        expected = {
            "range": {
                "price": {
                    "gte": 100,
                    "lte": 500,
                    "boost": 1.5,
                }
            }
        }
        assert result == expected

    def test_range_query_date_with_all_options(self):
        """날짜 범위 쿼리에 모든 옵션을 사용한 경우를 확인합니다."""
        result = RangeQuery.build(
            "created_at",
            gte="2024-01-01",
            lte="2024-12-31",
            format="yyyy-MM-dd",
            boost=2.0,
        )
        expected = {
            "range": {
                "created_at": {
                    "gte": "2024-01-01",
                    "lte": "2024-12-31",
                    "format": "yyyy-MM-dd",
                    "boost": 2.0,
                }
            }
        }
        assert result == expected

    def test_range_query_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = RangeQuery.build("price", gte=100)
        range_body = result["range"]["price"]
        assert "gte" in range_body
        assert "lte" not in range_body
        assert "gt" not in range_body
        assert "lt" not in range_body
        assert "format" not in range_body
        assert "boost" not in range_body

    def test_range_query_mixed_bounds(self):
        """gte와 lt를 혼합하여 사용한 범위 쿼리를 확인합니다."""
        result = RangeQuery.build("score", gte=0, lt=100)
        expected = {"range": {"score": {"gte": 0, "lt": 100}}}
        assert result == expected
