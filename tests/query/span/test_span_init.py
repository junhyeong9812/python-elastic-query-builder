"""query/span/__init__.py에 대한 단위 테스트.

Span 쿼리 패키지에서 모든 클래스를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestSpanQueryImports:
    """Span 쿼리 패키지 import 테스트."""

    def test_import_span_term_query(self):
        """query.span 패키지에서 SpanTermQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.span import SpanTermQuery
        assert SpanTermQuery is not None

    def test_import_span_near_query(self):
        """query.span 패키지에서 SpanNearQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.span import SpanNearQuery
        assert SpanNearQuery is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 모든 클래스를 포함하는지 확인합니다."""
        import elastic_query_builder.query.span as span_module
        expected_exports = ["SpanTermQuery", "SpanNearQuery"]
        for export in expected_exports:
            assert export in span_module.__all__, f"{export}이(가) __all__에 없습니다"

    def test_imported_classes_are_functional(self):
        """import한 클래스들이 실제로 동작하는지 확인합니다."""
        from elastic_query_builder.query.span import SpanTermQuery, SpanNearQuery

        # SpanTermQuery가 쿼리를 생성할 수 있는지 확인
        span_term_result = SpanTermQuery.build("field", "value")
        assert "span_term" in span_term_result

        # SpanNearQuery가 쿼리를 생성할 수 있는지 확인
        span_near_result = SpanNearQuery.build(
            clauses=[{"span_term": {"field": "value"}}], slop=1
        )
        assert "span_near" in span_near_result
