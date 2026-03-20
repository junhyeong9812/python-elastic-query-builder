"""query/nested.py에 대한 단위 테스트.

NestedQuery가 올바른 Elasticsearch nested 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.nested import NestedQuery


class TestNestedQuery:
    """NestedQuery 테스트."""

    def test_nested_basic(self):
        """기본 Nested 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = NestedQuery.build(
            "items", {"match": {"items.name": "test"}}
        )
        expected = {
            "nested": {
                "path": "items",
                "query": {"match": {"items.name": "test"}},
            }
        }
        assert result == expected

    def test_nested_with_score_mode(self):
        """score_mode 옵션이 포함된 Nested 쿼리가 올바르게 생성되는지 확인합니다."""
        result = NestedQuery.build(
            "comments",
            {"match": {"comments.text": {"query": "좋은 글"}}},
            score_mode="avg",
        )
        expected = {
            "nested": {
                "path": "comments",
                "query": {"match": {"comments.text": {"query": "좋은 글"}}},
                "score_mode": "avg",
            }
        }
        assert result == expected

    def test_nested_with_ignore_unmapped(self):
        """ignore_unmapped 옵션이 포함된 Nested 쿼리가 올바르게 생성되는지 확인합니다."""
        result = NestedQuery.build(
            "tags",
            {"term": {"tags.name": {"value": "python"}}},
            ignore_unmapped=True,
        )
        expected = {
            "nested": {
                "path": "tags",
                "query": {"term": {"tags.name": {"value": "python"}}},
                "ignore_unmapped": True,
            }
        }
        assert result == expected

    def test_nested_all_options(self):
        """모든 옵션이 포함된 Nested 쿼리가 올바르게 생성되는지 확인합니다."""
        result = NestedQuery.build(
            "items",
            {"range": {"items.price": {"gte": 100, "lte": 500}}},
            score_mode="max",
            ignore_unmapped=False,
        )
        expected = {
            "nested": {
                "path": "items",
                "query": {"range": {"items.price": {"gte": 100, "lte": 500}}},
                "score_mode": "max",
                "ignore_unmapped": False,
            }
        }
        assert result == expected

    def test_nested_without_score_mode_has_no_key(self):
        """score_mode를 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = NestedQuery.build("items", {"match_all": {}})
        assert "score_mode" not in result["nested"]

    def test_nested_without_ignore_unmapped_has_no_key(self):
        """ignore_unmapped를 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        result = NestedQuery.build("items", {"match_all": {}})
        assert "ignore_unmapped" not in result["nested"]

    def test_nested_structure(self):
        """Nested 쿼리 결과의 구조가 올바른지 확인합니다."""
        result = NestedQuery.build("items", {"match_all": {}})
        assert "nested" in result
        assert "path" in result["nested"]
        assert "query" in result["nested"]
        assert isinstance(result["nested"]["path"], str)
        assert isinstance(result["nested"]["query"], dict)

    def test_nested_with_bool_query(self):
        """Nested 쿼리 내부에 복잡한 bool 쿼리를 사용할 수 있는지 확인합니다."""
        bool_query = {
            "bool": {
                "must": [
                    {"match": {"items.name": {"query": "노트북"}}},
                    {"range": {"items.price": {"lte": 2000000}}},
                ]
            }
        }
        result = NestedQuery.build("items", bool_query, score_mode="sum")
        assert result["nested"]["path"] == "items"
        assert result["nested"]["query"] == bool_query
        assert result["nested"]["score_mode"] == "sum"
