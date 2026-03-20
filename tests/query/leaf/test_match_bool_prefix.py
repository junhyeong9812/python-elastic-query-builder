"""query/leaf/match_bool_prefix.py에 대한 단위 테스트.

MatchBoolPrefixQuery가 올바른 Elasticsearch 쿼리 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.match_bool_prefix import MatchBoolPrefixQuery


class TestMatchBoolPrefixQuery:
    """MatchBoolPrefixQuery 테스트."""

    def test_match_bool_prefix_basic(self):
        """기본 MatchBoolPrefix 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = MatchBoolPrefixQuery.build("title", "quick brown f")
        expected = {"match_bool_prefix": {"title": {"query": "quick brown f"}}}
        assert result == expected

    def test_match_bool_prefix_with_boost(self):
        """boost 옵션이 포함된 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchBoolPrefixQuery.build("title", "quick brown f", boost=1.5)
        expected = {
            "match_bool_prefix": {
                "title": {"query": "quick brown f", "boost": 1.5}
            }
        }
        assert result == expected

    def test_match_bool_prefix_with_all_options(self):
        """모든 옵션이 포함된 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchBoolPrefixQuery.build(
            "title", "quick brown f",
            boost=2.0,
            fuzziness="AUTO",
            operator="and",
            minimum_should_match="75%",
            analyzer="standard",
        )
        expected = {
            "match_bool_prefix": {
                "title": {
                    "query": "quick brown f",
                    "boost": 2.0,
                    "fuzziness": "AUTO",
                    "operator": "and",
                    "minimum_should_match": "75%",
                    "analyzer": "standard",
                }
            }
        }
        assert result == expected

    def test_match_bool_prefix_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = MatchBoolPrefixQuery.build("title", "quick brown f")
        body = result["match_bool_prefix"]["title"]
        assert "query" in body
        assert "boost" not in body
        assert "fuzziness" not in body
        assert "operator" not in body
        assert "minimum_should_match" not in body
        assert "analyzer" not in body

    def test_match_bool_prefix_with_fuzziness_only(self):
        """fuzziness만 지정한 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MatchBoolPrefixQuery.build("content", "tset", fuzziness="AUTO")
        expected = {
            "match_bool_prefix": {
                "content": {"query": "tset", "fuzziness": "AUTO"}
            }
        }
        assert result == expected
