"""query/leaf/exists.py에 대한 단위 테스트.

ExistsQuery가 올바른 Elasticsearch exists 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.exists import ExistsQuery


class TestExistsQuery:
    """ExistsQuery 테스트."""

    def test_exists_query(self):
        """기본 Exists 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = ExistsQuery.build("title")
        expected = {"exists": {"field": "title"}}
        assert result == expected

    def test_exists_query_nested_field(self):
        """중첩 필드에 대한 Exists 쿼리가 올바르게 생성되는지 확인합니다."""
        result = ExistsQuery.build("user.name")
        expected = {"exists": {"field": "user.name"}}
        assert result == expected

    def test_exists_query_structure(self):
        """Exists 쿼리 결과의 구조가 올바른지 확인합니다."""
        result = ExistsQuery.build("status")
        assert "exists" in result
        assert "field" in result["exists"]
        assert result["exists"]["field"] == "status"
