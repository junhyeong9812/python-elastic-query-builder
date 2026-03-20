"""aggregation/bucket/range.py에 대한 단위 테스트.

RangeAggregation이 올바른 Elasticsearch range 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.bucket.range import RangeAggregation


class TestRangeAggregation:
    """RangeAggregation 테스트."""

    def test_range_agg_basic(self):
        """기본 range 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = RangeAggregation.build(
            "price",
            ranges=[{"to": 100}, {"from": 100, "to": 200}, {"from": 200}],
        )
        expected = {
            "range": {
                "field": "price",
                "ranges": [
                    {"to": 100},
                    {"from": 100, "to": 200},
                    {"from": 200},
                ],
            }
        }
        assert result == expected

    def test_range_agg_keyed(self):
        """keyed 옵션이 포함된 range 집계가 올바르게 생성되는지 확인합니다."""
        result = RangeAggregation.build(
            "price",
            ranges=[{"to": 100}, {"from": 100}],
            keyed=True,
        )
        expected = {
            "range": {
                "field": "price",
                "ranges": [{"to": 100}, {"from": 100}],
                "keyed": True,
            }
        }
        assert result == expected

    def test_range_agg_without_keyed_has_no_key(self):
        """keyed를 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = RangeAggregation.build("price", ranges=[{"to": 50}])
        assert "keyed" not in result["range"]

    def test_range_agg_structure(self):
        """range 집계 결과의 구조가 올바른지 확인합니다."""
        result = RangeAggregation.build("price", ranges=[{"to": 100}])
        assert "range" in result
        assert "field" in result["range"]
        assert "ranges" in result["range"]
        assert isinstance(result["range"]["ranges"], list)

    def test_range_agg_with_named_ranges(self):
        """key가 지정된 range 집계가 올바르게 생성되는지 확인합니다."""
        result = RangeAggregation.build(
            "price",
            ranges=[
                {"key": "cheap", "to": 100},
                {"key": "moderate", "from": 100, "to": 500},
                {"key": "expensive", "from": 500},
            ],
        )
        assert len(result["range"]["ranges"]) == 3
        assert result["range"]["ranges"][0]["key"] == "cheap"
        assert result["range"]["ranges"][2]["key"] == "expensive"
