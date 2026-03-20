"""query/leaf/match.py에 대한 단위 테스트.

MatchQuery와 MatchPhraseQuery가 올바른 Elasticsearch 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.match import MatchQuery, MatchPhraseQuery


class TestMatchQuery:
    """MatchQuery 테스트."""

    def test_match_query_basic(self):
        """기본 Match 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = MatchQuery.build("title", "검색어")
        expected = {"match": {"title": {"query": "검색어"}}}
        assert result == expected

    def test_match_query_with_options(self):
        """모든 옵션이 포함된 Match 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchQuery.build(
            "title",
            "검색어",
            boost=2.0,
            operator="and",
            fuzziness="AUTO",
            analyzer="standard",
            minimum_should_match="75%",
        )
        expected = {
            "match": {
                "title": {
                    "query": "검색어",
                    "boost": 2.0,
                    "operator": "and",
                    "fuzziness": "AUTO",
                    "analyzer": "standard",
                    "minimum_should_match": "75%",
                }
            }
        }
        assert result == expected

    def test_match_query_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = MatchQuery.build("title", "검색어", boost=1.5)
        match_body = result["match"]["title"]
        assert "query" in match_body
        assert "boost" in match_body
        assert "fuzziness" not in match_body
        assert "operator" not in match_body
        assert "analyzer" not in match_body
        assert "minimum_should_match" not in match_body

    def test_match_query_with_boost_only(self):
        """boost만 지정한 Match 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchQuery.build("title", "검색어", boost=2.0)
        expected = {"match": {"title": {"query": "검색어", "boost": 2.0}}}
        assert result == expected

    def test_match_query_with_operator_only(self):
        """operator만 지정한 Match 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchQuery.build("title", "검색어", operator="and")
        expected = {"match": {"title": {"query": "검색어", "operator": "and"}}}
        assert result == expected

    def test_match_query_with_fuzziness_only(self):
        """fuzziness만 지정한 Match 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchQuery.build("content", "tset", fuzziness="AUTO")
        expected = {"match": {"content": {"query": "tset", "fuzziness": "AUTO"}}}
        assert result == expected


class TestMatchPhraseQuery:
    """MatchPhraseQuery 테스트."""

    def test_match_phrase_query_basic(self):
        """기본 MatchPhrase 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = MatchPhraseQuery.build("title", "빌더 패턴")
        expected = {"match_phrase": {"title": {"query": "빌더 패턴"}}}
        assert result == expected

    def test_match_phrase_query_with_options(self):
        """boost와 slop 옵션이 포함된 MatchPhrase 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchPhraseQuery.build("title", "빌더 패턴", boost=1.5, slop=2)
        expected = {
            "match_phrase": {
                "title": {
                    "query": "빌더 패턴",
                    "boost": 1.5,
                    "slop": 2,
                }
            }
        }
        assert result == expected

    def test_match_phrase_query_with_boost_only(self):
        """boost만 지정한 MatchPhrase 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchPhraseQuery.build("title", "빌더 패턴", boost=1.5)
        expected = {
            "match_phrase": {"title": {"query": "빌더 패턴", "boost": 1.5}}
        }
        assert result == expected

    def test_match_phrase_query_with_slop_only(self):
        """slop만 지정한 MatchPhrase 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchPhraseQuery.build("title", "빌더 패턴", slop=3)
        expected = {
            "match_phrase": {"title": {"query": "빌더 패턴", "slop": 3}}
        }
        assert result == expected

    def test_match_phrase_query_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = MatchPhraseQuery.build("title", "빌더 패턴")
        body = result["match_phrase"]["title"]
        assert "query" in body
        assert "boost" not in body
        assert "slop" not in body
