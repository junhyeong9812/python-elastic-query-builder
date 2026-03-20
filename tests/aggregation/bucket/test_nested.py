"""aggregation/bucket/nested.py에 대한 단위 테스트.

NestedAggregation이 올바른 Elasticsearch nested 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.bucket.nested import NestedAggregation


class TestNestedAggregation:
    """NestedAggregation 테스트."""

    def test_nested_agg_basic(self):
        """기본 nested 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = NestedAggregation.build("items")
        expected = {"nested": {"path": "items"}}
        assert result == expected

    def test_nested_agg_with_sub_aggs(self):
        """nested 집계의 결과를 하위 집계와 함께 사용하는 시나리오를 확인합니다.

        NestedAggregation.build()는 nested 집계 본문만 생성하며,
        하위 집계의 조합은 상위 레벨에서 수행합니다.
        """
        nested_agg = NestedAggregation.build("items")
        # 상위 레벨에서 하위 집계를 조합하는 예시
        agg_with_sub = {
            "nested_items": {
                **nested_agg,
                "aggs": {
                    "avg_price": {"avg": {"field": "items.price"}},
                },
            }
        }
        assert agg_with_sub["nested_items"]["nested"]["path"] == "items"
        assert "aggs" in agg_with_sub["nested_items"]
        assert "avg_price" in agg_with_sub["nested_items"]["aggs"]

    def test_nested_agg_structure(self):
        """nested 집계 결과의 구조가 올바른지 확인합니다."""
        result = NestedAggregation.build("comments")
        assert "nested" in result
        assert "path" in result["nested"]
        assert result["nested"]["path"] == "comments"

    def test_nested_agg_different_path(self):
        """다른 경로로 nested 집계를 생성할 수 있는지 확인합니다."""
        result = NestedAggregation.build("orders.items")
        expected = {"nested": {"path": "orders.items"}}
        assert result == expected
