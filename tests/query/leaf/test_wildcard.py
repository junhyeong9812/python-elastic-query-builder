"""query/leaf/wildcard.py에 대한 단위 테스트.

WildcardQuery가 올바른 Elasticsearch 와일드카드 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.wildcard import WildcardQuery


class TestWildcardQuery:
    """WildcardQuery 테스트."""

    def test_wildcard_query_basic(self):
        """기본 Wildcard 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = WildcardQuery.build("name", "test*")
        expected = {"wildcard": {"name": {"value": "test*"}}}
        assert result == expected

    def test_wildcard_query_with_boost(self):
        """boost 옵션이 포함된 Wildcard 쿼리가 올바르게 생성되는지 확인합니다."""
        result = WildcardQuery.build("name", "test*", boost=1.5)
        expected = {"wildcard": {"name": {"value": "test*", "boost": 1.5}}}
        assert result == expected

    def test_wildcard_query_case_insensitive(self):
        """대소문자 무시 옵션이 포함된 Wildcard 쿼리가 올바르게 생성되는지 확인합니다."""
        result = WildcardQuery.build("name", "Test*", case_insensitive=True)
        expected = {
            "wildcard": {
                "name": {
                    "value": "Test*",
                    "case_insensitive": True,
                }
            }
        }
        assert result == expected

    def test_wildcard_query_with_question_mark(self):
        """물음표 와일드카드 패턴이 올바르게 처리되는지 확인합니다."""
        result = WildcardQuery.build("code", "A?B")
        expected = {"wildcard": {"code": {"value": "A?B"}}}
        assert result == expected

    def test_wildcard_query_with_all_options(self):
        """모든 옵션을 사용한 Wildcard 쿼리가 올바르게 생성되는지 확인합니다."""
        result = WildcardQuery.build(
            "email", "*@example.com", boost=2.0, case_insensitive=True
        )
        expected = {
            "wildcard": {
                "email": {
                    "value": "*@example.com",
                    "boost": 2.0,
                    "case_insensitive": True,
                }
            }
        }
        assert result == expected

    def test_wildcard_query_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = WildcardQuery.build("name", "test*")
        body = result["wildcard"]["name"]
        assert "value" in body
        assert "boost" not in body
        assert "case_insensitive" not in body
