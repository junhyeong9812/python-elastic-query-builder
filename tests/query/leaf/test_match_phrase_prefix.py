"""query/leaf/match_phrase_prefix.py에 대한 단위 테스트.

MatchPhrasePrefixQuery가 올바른 Elasticsearch 쿼리 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.match_phrase_prefix import MatchPhrasePrefixQuery


class TestMatchPhrasePrefixQuery:
    """MatchPhrasePrefixQuery 테스트."""

    def test_match_phrase_prefix_basic(self):
        """기본 MatchPhrasePrefix 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = MatchPhrasePrefixQuery.build("title", "빌더 패")
        expected = {"match_phrase_prefix": {"title": {"query": "빌더 패"}}}
        assert result == expected

    def test_match_phrase_prefix_with_max_expansions(self):
        """max_expansions 옵션이 포함된 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchPhrasePrefixQuery.build("title", "빌더 패", max_expansions=10)
        expected = {
            "match_phrase_prefix": {
                "title": {"query": "빌더 패", "max_expansions": 10}
            }
        }
        assert result == expected

    def test_match_phrase_prefix_with_all_options(self):
        """모든 옵션이 포함된 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchPhrasePrefixQuery.build(
            "title", "빌더 패",
            max_expansions=50,
            boost=1.5,
            slop=2,
            analyzer="standard",
        )
        expected = {
            "match_phrase_prefix": {
                "title": {
                    "query": "빌더 패",
                    "max_expansions": 50,
                    "boost": 1.5,
                    "slop": 2,
                    "analyzer": "standard",
                }
            }
        }
        assert result == expected

    def test_match_phrase_prefix_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = MatchPhrasePrefixQuery.build("title", "빌더 패")
        body = result["match_phrase_prefix"]["title"]
        assert "query" in body
        assert "max_expansions" not in body
        assert "boost" not in body
        assert "slop" not in body
        assert "analyzer" not in body

    def test_match_phrase_prefix_with_boost_only(self):
        """boost만 지정한 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchPhrasePrefixQuery.build("title", "빌더 패", boost=2.0)
        expected = {
            "match_phrase_prefix": {
                "title": {"query": "빌더 패", "boost": 2.0}
            }
        }
        assert result == expected
