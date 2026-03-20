"""query/leaf/simple_query_string.py에 대한 단위 테스트.

SimpleQueryStringQuery가 올바른 Elasticsearch 쿼리 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.simple_query_string import SimpleQueryStringQuery


class TestSimpleQueryStringQuery:
    """SimpleQueryStringQuery 테스트."""

    def test_simple_query_string_basic(self):
        """기본 simple_query_string 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = SimpleQueryStringQuery.build('"fried eggs" +(eggplant | potato) -frittata')
        expected = {
            "simple_query_string": {
                "query": '"fried eggs" +(eggplant | potato) -frittata',
            }
        }
        assert result == expected

    def test_simple_query_string_with_fields(self):
        """fields를 지정한 simple_query_string 쿼리를 확인합니다."""
        result = SimpleQueryStringQuery.build(
            "foo bar", fields=["title^5", "body"],
        )
        expected = {
            "simple_query_string": {
                "query": "foo bar",
                "fields": ["title^5", "body"],
            }
        }
        assert result == expected

    def test_simple_query_string_with_default_operator(self):
        """default_operator를 지정한 simple_query_string 쿼리를 확인합니다."""
        result = SimpleQueryStringQuery.build(
            "foo bar baz", default_operator="AND",
        )
        expected = {
            "simple_query_string": {
                "query": "foo bar baz",
                "default_operator": "AND",
            }
        }
        assert result == expected

    def test_simple_query_string_with_flags(self):
        """flags를 지정한 simple_query_string 쿼리를 확인합니다."""
        result = SimpleQueryStringQuery.build(
            "foo | bar + baz*",
            flags="OR|AND|PREFIX",
        )
        expected = {
            "simple_query_string": {
                "query": "foo | bar + baz*",
                "flags": "OR|AND|PREFIX",
            }
        }
        assert result == expected

    def test_simple_query_string_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = SimpleQueryStringQuery.build("test")
        body = result["simple_query_string"]
        assert "query" in body
        assert "fields" not in body
        assert "default_operator" not in body
        assert "analyzer" not in body
        assert "flags" not in body
        assert "minimum_should_match" not in body
        assert "boost" not in body
