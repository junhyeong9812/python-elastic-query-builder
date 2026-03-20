"""query/span/span_near.py에 대한 단위 테스트.

SpanNearQuery가 올바른 Elasticsearch span_near 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.span.span_near import SpanNearQuery


class TestSpanNearQuery:
    """SpanNearQuery 테스트."""

    def test_span_near_basic(self):
        """기본 SpanNear 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        span1 = {"span_term": {"content": "검색"}}
        span2 = {"span_term": {"content": "엔진"}}
        result = SpanNearQuery.build(clauses=[span1, span2], slop=3)
        expected = {
            "span_near": {
                "clauses": [
                    {"span_term": {"content": "검색"}},
                    {"span_term": {"content": "엔진"}},
                ],
                "slop": 3,
            }
        }
        assert result == expected

    def test_span_near_in_order(self):
        """in_order 옵션이 포함된 SpanNear 쿼리가 올바르게 생성되는지 확인합니다."""
        span1 = {"span_term": {"content": "빠른"}}
        span2 = {"span_term": {"content": "검색"}}
        result = SpanNearQuery.build(clauses=[span1, span2], slop=2, in_order=True)
        expected = {
            "span_near": {
                "clauses": [
                    {"span_term": {"content": "빠른"}},
                    {"span_term": {"content": "검색"}},
                ],
                "slop": 2,
                "in_order": True,
            }
        }
        assert result == expected

    def test_span_near_in_order_false(self):
        """in_order=False가 올바르게 반영되는지 확인합니다."""
        span1 = {"span_term": {"content": "foo"}}
        span2 = {"span_term": {"content": "bar"}}
        result = SpanNearQuery.build(clauses=[span1, span2], slop=5, in_order=False)
        assert result["span_near"]["in_order"] is False

    def test_span_near_with_boost(self):
        """boost 옵션이 포함된 SpanNear 쿼리가 올바르게 생성되는지 확인합니다."""
        span1 = {"span_term": {"content": "elastic"}}
        span2 = {"span_term": {"content": "search"}}
        result = SpanNearQuery.build(clauses=[span1, span2], slop=1, boost=1.5)
        expected = {
            "span_near": {
                "clauses": [
                    {"span_term": {"content": "elastic"}},
                    {"span_term": {"content": "search"}},
                ],
                "slop": 1,
                "boost": 1.5,
            }
        }
        assert result == expected

    def test_span_near_all_options(self):
        """모든 옵션이 포함된 SpanNear 쿼리가 올바르게 생성되는지 확인합니다."""
        span1 = {"span_term": {"content": "hello"}}
        span2 = {"span_term": {"content": "world"}}
        result = SpanNearQuery.build(
            clauses=[span1, span2], slop=4, in_order=True, boost=2.0
        )
        expected = {
            "span_near": {
                "clauses": [
                    {"span_term": {"content": "hello"}},
                    {"span_term": {"content": "world"}},
                ],
                "slop": 4,
                "in_order": True,
                "boost": 2.0,
            }
        }
        assert result == expected

    def test_span_near_without_in_order_has_no_key(self):
        """in_order를 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        span1 = {"span_term": {"content": "foo"}}
        result = SpanNearQuery.build(clauses=[span1], slop=1)
        assert "in_order" not in result["span_near"]

    def test_span_near_without_boost_has_no_key(self):
        """boost를 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        span1 = {"span_term": {"content": "foo"}}
        result = SpanNearQuery.build(clauses=[span1], slop=1)
        assert "boost" not in result["span_near"]

    def test_span_near_structure(self):
        """SpanNear 쿼리 결과의 구조가 올바른지 확인합니다."""
        span1 = {"span_term": {"content": "foo"}}
        result = SpanNearQuery.build(clauses=[span1], slop=2)
        assert "span_near" in result
        assert "clauses" in result["span_near"]
        assert "slop" in result["span_near"]
        assert isinstance(result["span_near"]["clauses"], list)
        assert isinstance(result["span_near"]["slop"], int)
