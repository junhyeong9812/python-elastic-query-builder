"""query/leaf/combined_fields.py에 대한 단위 테스트.

CombinedFieldsQuery가 올바른 Elasticsearch 쿼리 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.combined_fields import CombinedFieldsQuery


class TestCombinedFieldsQuery:
    """CombinedFieldsQuery 테스트."""

    def test_combined_fields_basic(self):
        """기본 combined_fields 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = CombinedFieldsQuery.build(
            "database systems", ["title", "abstract", "body"],
        )
        expected = {
            "combined_fields": {
                "query": "database systems",
                "fields": ["title", "abstract", "body"],
            }
        }
        assert result == expected

    def test_combined_fields_with_operator(self):
        """operator를 지정한 combined_fields 쿼리를 확인합니다."""
        result = CombinedFieldsQuery.build(
            "database systems", ["title", "abstract"], operator="and",
        )
        expected = {
            "combined_fields": {
                "query": "database systems",
                "fields": ["title", "abstract"],
                "operator": "and",
            }
        }
        assert result == expected

    def test_combined_fields_with_minimum_should_match(self):
        """minimum_should_match를 지정한 combined_fields 쿼리를 확인합니다."""
        result = CombinedFieldsQuery.build(
            "database systems", ["title", "body"],
            minimum_should_match=2,
        )
        expected = {
            "combined_fields": {
                "query": "database systems",
                "fields": ["title", "body"],
                "minimum_should_match": 2,
            }
        }
        assert result == expected

    def test_combined_fields_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = CombinedFieldsQuery.build("test", ["f1", "f2"])
        body = result["combined_fields"]
        assert "query" in body
        assert "fields" in body
        assert "operator" not in body
        assert "minimum_should_match" not in body
        assert "boost" not in body
