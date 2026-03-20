"""query/specialized/more_like_this.py에 대한 단위 테스트.

MoreLikeThisQuery가 올바른 Elasticsearch more_like_this 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.specialized.more_like_this import MoreLikeThisQuery


class TestMoreLikeThisQuery:
    """MoreLikeThisQuery 테스트."""

    def test_basic(self):
        """기본 more_like_this 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = MoreLikeThisQuery.build(
            fields=["title", "description"],
            like="검색 엔진 최적화",
        )
        expected = {
            "more_like_this": {
                "fields": ["title", "description"],
                "like": "검색 엔진 최적화",
            }
        }
        assert result == expected

    def test_with_min_term_freq(self):
        """min_term_freq 옵션이 올바르게 설정되는지 확인합니다."""
        result = MoreLikeThisQuery.build(
            fields=["content"],
            like="Elasticsearch tutorial",
            min_term_freq=2,
        )
        assert result["more_like_this"]["min_term_freq"] == 2

    def test_with_min_doc_freq_and_max_query_terms(self):
        """min_doc_freq와 max_query_terms가 올바르게 설정되는지 확인합니다."""
        result = MoreLikeThisQuery.build(
            fields=["title"],
            like="Python programming",
            min_doc_freq=5,
            max_query_terms=25,
        )
        body = result["more_like_this"]
        assert body["min_doc_freq"] == 5
        assert body["max_query_terms"] == 25

    def test_with_minimum_should_match_and_boost(self):
        """minimum_should_match와 boost가 올바르게 설정되는지 확인합니다."""
        result = MoreLikeThisQuery.build(
            fields=["title"],
            like="test",
            minimum_should_match="30%",
            boost=1.5,
        )
        body = result["more_like_this"]
        assert body["minimum_should_match"] == "30%"
        assert body["boost"] == 1.5

    def test_like_with_document_object(self):
        """like 파라미터에 문서 객체를 전달할 수 있는지 확인합니다."""
        like_doc = {"_index": "my_index", "_id": "1"}
        result = MoreLikeThisQuery.build(
            fields=["title", "description"],
            like=like_doc,
        )
        assert result["more_like_this"]["like"] == like_doc

    def test_all_optional_params(self):
        """모든 선택적 파라미터가 올바르게 설정되는지 확인합니다."""
        result = MoreLikeThisQuery.build(
            fields=["title"],
            like="test query",
            min_term_freq=1,
            min_doc_freq=3,
            max_query_terms=10,
            minimum_should_match="50%",
            boost=2.0,
        )
        body = result["more_like_this"]
        assert body["fields"] == ["title"]
        assert body["like"] == "test query"
        assert body["min_term_freq"] == 1
        assert body["min_doc_freq"] == 3
        assert body["max_query_terms"] == 10
        assert body["minimum_should_match"] == "50%"
        assert body["boost"] == 2.0

    def test_optional_params_not_included_when_none(self):
        """None인 선택적 파라미터가 결과에 포함되지 않는지 확인합니다."""
        result = MoreLikeThisQuery.build(
            fields=["title"],
            like="test",
        )
        body = result["more_like_this"]
        assert "min_term_freq" not in body
        assert "min_doc_freq" not in body
        assert "max_query_terms" not in body
        assert "minimum_should_match" not in body
        assert "boost" not in body
