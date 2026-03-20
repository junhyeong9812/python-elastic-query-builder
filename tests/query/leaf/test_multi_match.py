"""query/leaf/multi_match.py에 대한 단위 테스트.

MultiMatchQuery가 올바른 Elasticsearch 쿼리 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.multi_match import MultiMatchQuery
from elastic_query_builder.core.enums import MultiMatchType


class TestMultiMatchQuery:
    """MultiMatchQuery 테스트."""

    def test_multi_match_basic(self):
        """기본 MultiMatch 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = MultiMatchQuery.build(["title", "content"], "검색어")
        expected = {
            "multi_match": {
                "query": "검색어",
                "fields": ["title", "content"],
            }
        }
        assert result == expected

    def test_multi_match_with_type(self):
        """type 옵션이 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"], "검색어", type="best_fields"
        )
        expected = {
            "multi_match": {
                "query": "검색어",
                "fields": ["title", "content"],
                "type": "best_fields",
            }
        }
        assert result == expected

    def test_multi_match_with_enum_type(self):
        """MultiMatchType 열거형을 사용한 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"], "검색어", type=MultiMatchType.CROSS_FIELDS
        )
        body = result["multi_match"]
        assert body["type"] == "cross_fields"

    def test_multi_match_with_tie_breaker(self):
        """tie_breaker 옵션이 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"], "검색어", tie_breaker=0.3
        )
        assert result["multi_match"]["tie_breaker"] == 0.3

    def test_multi_match_with_boost(self):
        """boost 옵션이 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"], "검색어", boost=1.5
        )
        assert result["multi_match"]["boost"] == 1.5

    def test_multi_match_with_fuzziness(self):
        """fuzziness 옵션이 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"], "tset", fuzziness="AUTO"
        )
        assert result["multi_match"]["fuzziness"] == "AUTO"

    def test_multi_match_with_operator(self):
        """operator 옵션이 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"], "검색어", operator="and"
        )
        assert result["multi_match"]["operator"] == "and"

    def test_multi_match_with_fields_boost_notation(self):
        """필드 부스트 표기법이 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title^3", "content^1", "description^0.5"], "검색어"
        )
        assert result["multi_match"]["fields"] == [
            "title^3", "content^1", "description^0.5"
        ]

    def test_multi_match_with_all_options(self):
        """모든 옵션이 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"],
            "검색어",
            type="most_fields",
            tie_breaker=0.3,
            boost=2.0,
            fuzziness="AUTO",
            operator="or",
            minimum_should_match="75%",
            analyzer="standard",
            max_expansions=50,
            prefix_length=1,
            zero_terms_query="none",
        )
        expected = {
            "multi_match": {
                "query": "검색어",
                "fields": ["title", "content"],
                "type": "most_fields",
                "tie_breaker": 0.3,
                "boost": 2.0,
                "fuzziness": "AUTO",
                "operator": "or",
                "minimum_should_match": "75%",
                "analyzer": "standard",
                "max_expansions": 50,
                "prefix_length": 1,
                "zero_terms_query": "none",
            }
        }
        assert result == expected

    def test_multi_match_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = MultiMatchQuery.build(["title", "content"], "검색어")
        body = result["multi_match"]
        assert "query" in body
        assert "fields" in body
        assert "type" not in body
        assert "tie_breaker" not in body
        assert "boost" not in body
        assert "fuzziness" not in body
        assert "operator" not in body
        assert "minimum_should_match" not in body
        assert "analyzer" not in body
        assert "max_expansions" not in body
        assert "prefix_length" not in body
        assert "zero_terms_query" not in body

    def test_multi_match_with_minimum_should_match(self):
        """minimum_should_match 옵션이 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"], "검색어", minimum_should_match="2"
        )
        assert result["multi_match"]["minimum_should_match"] == "2"

    def test_multi_match_with_max_expansions_and_prefix_length(self):
        """max_expansions와 prefix_length가 포함된 MultiMatch 쿼리가 올바르게 생성되는지 확인합니다."""
        result = MultiMatchQuery.build(
            ["title", "content"],
            "검색어",
            type="phrase_prefix",
            max_expansions=10,
            prefix_length=2,
        )
        body = result["multi_match"]
        assert body["type"] == "phrase_prefix"
        assert body["max_expansions"] == 10
        assert body["prefix_length"] == 2
