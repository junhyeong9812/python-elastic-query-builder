"""query/span/span_term.py에 대한 단위 테스트.

SpanTermQuery가 올바른 Elasticsearch span_term 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.span.span_term import SpanTermQuery


class TestSpanTermQuery:
    """SpanTermQuery 테스트."""

    def test_span_term_basic(self):
        """기본 SpanTerm 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = SpanTermQuery.build("content", "검색")
        expected = {"span_term": {"content": "검색"}}
        assert result == expected

    def test_span_term_english(self):
        """영어 값으로 SpanTerm 쿼리를 생성할 수 있는지 확인합니다."""
        result = SpanTermQuery.build("title", "elasticsearch")
        expected = {"span_term": {"title": "elasticsearch"}}
        assert result == expected

    def test_span_term_different_field(self):
        """다른 필드명으로 SpanTerm 쿼리를 생성할 수 있는지 확인합니다."""
        result = SpanTermQuery.build("description", "패턴")
        expected = {"span_term": {"description": "패턴"}}
        assert result == expected

    def test_span_term_structure(self):
        """SpanTerm 쿼리 결과의 구조가 올바른지 확인합니다."""
        result = SpanTermQuery.build("content", "test")
        assert "span_term" in result
        assert "content" in result["span_term"]
        assert result["span_term"]["content"] == "test"
