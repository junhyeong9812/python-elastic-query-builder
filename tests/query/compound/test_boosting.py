"""query/compound/boosting.py에 대한 단위 테스트.

BoostingQuery가 올바른 Elasticsearch boosting 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.compound.boosting import BoostingQuery


class TestBoostingQuery:
    """BoostingQuery 테스트."""

    def test_boosting_basic(self):
        """기본 Boosting 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        positive = {"match": {"title": {"query": "apple"}}}
        negative = {"match": {"title": {"query": "pie"}}}
        result = BoostingQuery.build(
            positive=positive, negative=negative, negative_boost=0.5,
        )
        expected = {
            "boosting": {
                "positive": {"match": {"title": {"query": "apple"}}},
                "negative": {"match": {"title": {"query": "pie"}}},
                "negative_boost": 0.5,
            }
        }
        assert result == expected

    def test_boosting_negative_boost_value(self):
        """negative_boost 값이 올바르게 설정되는지 확인합니다."""
        positive = {"match_all": {}}
        negative = {"term": {"status": {"value": "deprecated"}}}
        result = BoostingQuery.build(
            positive=positive, negative=negative, negative_boost=0.2,
        )
        assert result["boosting"]["negative_boost"] == 0.2

    def test_boosting_structure(self):
        """Boosting 쿼리 결과의 구조가 올바른지 확인합니다."""
        positive = {"match_all": {}}
        negative = {"term": {"status": {"value": "old"}}}
        result = BoostingQuery.build(
            positive=positive, negative=negative, negative_boost=0.5,
        )
        assert "boosting" in result
        assert "positive" in result["boosting"]
        assert "negative" in result["boosting"]
        assert "negative_boost" in result["boosting"]

    def test_boosting_with_complex_queries(self):
        """복잡한 쿼리를 사용한 Boosting 쿼리가 올바르게 생성되는지 확인합니다."""
        positive = {
            "bool": {
                "must": [
                    {"match": {"title": {"query": "elasticsearch"}}},
                    {"range": {"date": {"gte": "2024-01-01"}}},
                ]
            }
        }
        negative = {
            "bool": {
                "should": [
                    {"term": {"status": {"value": "draft"}}},
                    {"term": {"status": {"value": "archived"}}},
                ]
            }
        }
        result = BoostingQuery.build(
            positive=positive, negative=negative, negative_boost=0.3,
        )
        expected = {
            "boosting": {
                "positive": positive,
                "negative": negative,
                "negative_boost": 0.3,
            }
        }
        assert result == expected
