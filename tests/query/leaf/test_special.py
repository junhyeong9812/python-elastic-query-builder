"""query/leaf/special.py에 대한 단위 테스트.

MatchAllQuery와 MatchNoneQuery가 올바른 Elasticsearch 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.special import MatchAllQuery, MatchNoneQuery


class TestMatchAllQuery:
    """MatchAllQuery 테스트."""

    def test_match_all_query(self):
        """기본 MatchAll 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = MatchAllQuery.build()
        expected = {"match_all": {}}
        assert result == expected

    def test_match_all_query_with_boost(self):
        """boost 옵션이 포함된 MatchAll 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchAllQuery.build(boost=1.5)
        expected = {"match_all": {"boost": 1.5}}
        assert result == expected

    def test_match_all_query_without_boost_is_empty_body(self):
        """boost 없이 생성하면 match_all의 본문이 빈 딕셔너리인지 확인합니다."""
        result = MatchAllQuery.build()
        assert result["match_all"] == {}

    def test_match_all_query_structure(self):
        """MatchAll 쿼리 결과의 구조가 올바른지 확인합니다."""
        result = MatchAllQuery.build()
        assert "match_all" in result
        assert isinstance(result["match_all"], dict)


class TestMatchNoneQuery:
    """MatchNoneQuery 테스트."""

    def test_match_none_query(self):
        """기본 MatchNone 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = MatchNoneQuery.build()
        expected = {"match_none": {}}
        assert result == expected

    def test_match_none_query_structure(self):
        """MatchNone 쿼리 결과의 구조가 올바른지 확인합니다."""
        result = MatchNoneQuery.build()
        assert "match_none" in result
        assert isinstance(result["match_none"], dict)

    def test_match_none_query_body_is_empty(self):
        """MatchNone 쿼리의 본문이 항상 빈 딕셔너리인지 확인합니다."""
        result = MatchNoneQuery.build()
        assert result["match_none"] == {}
