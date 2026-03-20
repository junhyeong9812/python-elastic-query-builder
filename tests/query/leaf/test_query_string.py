"""query/leaf/query_string.py에 대한 단위 테스트.

QueryStringQuery가 올바른 Elasticsearch 쿼리 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.query_string import QueryStringQuery


class TestQueryStringQuery:
    """QueryStringQuery 테스트."""

    def test_query_string_basic(self):
        """기본 query_string 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = QueryStringQuery.build("status:active")
        expected = {"query_string": {"query": "status:active"}}
        assert result == expected

    def test_query_string_with_fields(self):
        """fields를 지정한 query_string 쿼리를 확인합니다."""
        result = QueryStringQuery.build(
            "quick brown fox", fields=["title", "content"],
        )
        expected = {
            "query_string": {
                "query": "quick brown fox",
                "fields": ["title", "content"],
            }
        }
        assert result == expected

    def test_query_string_with_default_operator(self):
        """default_operator를 지정한 query_string 쿼리를 확인합니다."""
        result = QueryStringQuery.build(
            "quick brown fox", default_operator="AND",
        )
        expected = {
            "query_string": {
                "query": "quick brown fox",
                "default_operator": "AND",
            }
        }
        assert result == expected

    def test_query_string_with_fuzziness(self):
        """fuzziness를 지정한 query_string 쿼리를 확인합니다."""
        result = QueryStringQuery.build("quikc~", fuzziness="AUTO")
        expected = {
            "query_string": {
                "query": "quikc~",
                "fuzziness": "AUTO",
            }
        }
        assert result == expected

    def test_query_string_with_all_options(self):
        """모든 옵션이 포함된 query_string 쿼리를 확인합니다."""
        result = QueryStringQuery.build(
            "test query",
            fields=["title^2", "content"],
            default_field="title",
            default_operator="AND",
            analyzer="standard",
            allow_leading_wildcard=False,
            fuzziness="AUTO",
            boost=2.0,
            minimum_should_match="75%",
        )
        body = result["query_string"]
        assert body["query"] == "test query"
        assert body["fields"] == ["title^2", "content"]
        assert body["default_field"] == "title"
        assert body["default_operator"] == "AND"
        assert body["analyzer"] == "standard"
        assert body["allow_leading_wildcard"] is False
        assert body["fuzziness"] == "AUTO"
        assert body["boost"] == 2.0
        assert body["minimum_should_match"] == "75%"

    def test_query_string_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = QueryStringQuery.build("test")
        body = result["query_string"]
        assert "query" in body
        assert "fields" not in body
        assert "default_field" not in body
        assert "default_operator" not in body
        assert "analyzer" not in body
        assert "allow_leading_wildcard" not in body
        assert "fuzziness" not in body
        assert "boost" not in body
        assert "minimum_should_match" not in body
