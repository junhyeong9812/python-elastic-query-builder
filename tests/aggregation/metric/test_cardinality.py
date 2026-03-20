"""aggregation/metric/cardinality.py에 대한 단위 테스트.

CardinalityAggregation이 올바른 Elasticsearch cardinality 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.metric.cardinality import CardinalityAggregation


class TestCardinalityAggregation:
    """CardinalityAggregation 테스트."""

    def test_cardinality_basic(self):
        """기본 cardinality 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = CardinalityAggregation.build("user_id")
        expected = {"cardinality": {"field": "user_id"}}
        assert result == expected

    def test_cardinality_with_precision(self):
        """precision_threshold 옵션이 포함된 cardinality 집계가 올바르게 생성되는지 확인합니다."""
        result = CardinalityAggregation.build("user_id", precision_threshold=100)
        expected = {
            "cardinality": {
                "field": "user_id",
                "precision_threshold": 100,
            }
        }
        assert result == expected

    def test_cardinality_with_missing(self):
        """missing 옵션이 포함된 cardinality 집계가 올바르게 생성되는지 확인합니다."""
        result = CardinalityAggregation.build("user_id", missing="unknown")
        expected = {
            "cardinality": {
                "field": "user_id",
                "missing": "unknown",
            }
        }
        assert result == expected

    def test_cardinality_all_options(self):
        """모든 옵션이 포함된 cardinality 집계가 올바르게 생성되는지 확인합니다."""
        result = CardinalityAggregation.build(
            "user_id", precision_threshold=200, missing="N/A"
        )
        expected = {
            "cardinality": {
                "field": "user_id",
                "precision_threshold": 200,
                "missing": "N/A",
            }
        }
        assert result == expected

    def test_cardinality_without_optional_has_no_keys(self):
        """선택 옵션을 지정하지 않으면 결과에 해당 키가 없는지 확인합니다."""
        result = CardinalityAggregation.build("user_id")
        body = result["cardinality"]
        assert "precision_threshold" not in body
        assert "missing" not in body

    def test_cardinality_structure(self):
        """cardinality 집계 결과의 구조가 올바른지 확인합니다."""
        result = CardinalityAggregation.build("session_id")
        assert "cardinality" in result
        assert "field" in result["cardinality"]
        assert result["cardinality"]["field"] == "session_id"
