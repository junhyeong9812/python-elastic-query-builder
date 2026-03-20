"""query/leaf/prefix.py에 대한 단위 테스트.

PrefixQuery가 올바른 Elasticsearch 접두사 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.prefix import PrefixQuery


class TestPrefixQuery:
    """PrefixQuery 테스트."""

    def test_prefix_query_basic(self):
        """기본 Prefix 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = PrefixQuery.build("name", "test")
        expected = {"prefix": {"name": {"value": "test"}}}
        assert result == expected

    def test_prefix_query_with_boost(self):
        """boost 옵션이 포함된 Prefix 쿼리가 올바르게 생성되는지 확인합니다."""
        result = PrefixQuery.build("name", "test", boost=1.5)
        expected = {"prefix": {"name": {"value": "test", "boost": 1.5}}}
        assert result == expected

    def test_prefix_query_case_insensitive(self):
        """대소문자 무시 옵션이 포함된 Prefix 쿼리가 올바르게 생성되는지 확인합니다."""
        result = PrefixQuery.build("name", "Test", case_insensitive=True)
        expected = {
            "prefix": {
                "name": {
                    "value": "Test",
                    "case_insensitive": True,
                }
            }
        }
        assert result == expected

    def test_prefix_query_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = PrefixQuery.build("name", "test")
        body = result["prefix"]["name"]
        assert "value" in body
        assert "boost" not in body
        assert "case_insensitive" not in body
