"""query/leaf/term.py에 대한 단위 테스트.

TermQuery와 TermsQuery가 올바른 Elasticsearch 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.term import TermQuery, TermsQuery


class TestTermQuery:
    """TermQuery 테스트."""

    def test_term_query_basic(self):
        """기본 Term 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = TermQuery.build("status", "active")
        expected = {"term": {"status": {"value": "active"}}}
        assert result == expected

    def test_term_query_with_boost(self):
        """boost 옵션이 포함된 Term 쿼리가 올바르게 생성되는지 확인합니다."""
        result = TermQuery.build("status", "active", boost=1.5)
        expected = {"term": {"status": {"value": "active", "boost": 1.5}}}
        assert result == expected

    def test_term_query_with_numeric_value(self):
        """숫자 값으로 Term 쿼리를 생성할 수 있는지 확인합니다."""
        result = TermQuery.build("age", 25)
        expected = {"term": {"age": {"value": 25}}}
        assert result == expected

    def test_term_query_with_boolean_value(self):
        """불리언 값으로 Term 쿼리를 생성할 수 있는지 확인합니다."""
        result = TermQuery.build("is_active", True)
        expected = {"term": {"is_active": {"value": True}}}
        assert result == expected

    def test_term_query_without_boost_has_no_boost_key(self):
        """boost를 지정하지 않으면 결과에 boost 키가 없는지 확인합니다."""
        result = TermQuery.build("status", "active")
        assert "boost" not in result["term"]["status"]


class TestTermsQuery:
    """TermsQuery 테스트."""

    def test_terms_query_basic(self):
        """기본 Terms 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = TermsQuery.build("status", ["active", "pending"])
        expected = {"terms": {"status": ["active", "pending"]}}
        assert result == expected

    def test_terms_query_with_boost(self):
        """boost 옵션이 포함된 Terms 쿼리가 올바르게 생성되는지 확인합니다."""
        result = TermsQuery.build("status", ["active"], boost=2.0)
        expected = {"terms": {"status": ["active"], "boost": 2.0}}
        assert result == expected

    def test_terms_query_single_value(self):
        """단일 값 리스트로 Terms 쿼리를 생성할 수 있는지 확인합니다."""
        result = TermsQuery.build("color", ["red"])
        expected = {"terms": {"color": ["red"]}}
        assert result == expected

    def test_terms_query_numeric_values(self):
        """숫자 값 리스트로 Terms 쿼리를 생성할 수 있는지 확인합니다."""
        result = TermsQuery.build("code", [1, 2, 3])
        expected = {"terms": {"code": [1, 2, 3]}}
        assert result == expected

    def test_terms_query_without_boost_has_no_boost_key(self):
        """boost를 지정하지 않으면 결과에 boost 키가 없는지 확인합니다."""
        result = TermsQuery.build("status", ["active"])
        assert "boost" not in result["terms"]
