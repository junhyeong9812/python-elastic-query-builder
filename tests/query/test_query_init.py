"""query/__init__.py에 대한 단위 테스트.

전체 쿼리 패키지에서 모든 클래스를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestQueryPackageImports:
    """쿼리 패키지 전체 import 테스트."""

    def test_import_leaf_queries(self):
        """query 패키지에서 리프 쿼리 클래스를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query import (
            TermQuery, TermsQuery, MatchQuery, MatchPhraseQuery,
            RangeQuery, WildcardQuery, ExistsQuery, IdsQuery,
            MatchAllQuery, MatchNoneQuery,
        )
        assert TermQuery is not None
        assert TermsQuery is not None
        assert MatchQuery is not None
        assert MatchPhraseQuery is not None
        assert RangeQuery is not None
        assert WildcardQuery is not None
        assert ExistsQuery is not None
        assert IdsQuery is not None
        assert MatchAllQuery is not None
        assert MatchNoneQuery is not None

    def test_import_compound_queries(self):
        """query 패키지에서 복합 쿼리 클래스를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query import BoolQueryBuilder, DisMaxQuery
        assert BoolQueryBuilder is not None
        assert DisMaxQuery is not None

    def test_import_span_queries(self):
        """query 패키지에서 Span 쿼리 클래스를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query import SpanTermQuery, SpanNearQuery
        assert SpanTermQuery is not None
        assert SpanNearQuery is not None

    def test_import_nested_query(self):
        """query 패키지에서 NestedQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query import NestedQuery
        assert NestedQuery is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 모든 클래스를 포함하는지 확인합니다."""
        import elastic_query_builder.query as query_module
        expected_exports = [
            "TermQuery", "TermsQuery", "MatchQuery", "MatchPhraseQuery",
            "RangeQuery", "WildcardQuery", "ExistsQuery", "IdsQuery",
            "MatchAllQuery", "MatchNoneQuery",
            "BoolQueryBuilder", "DisMaxQuery",
            "SpanTermQuery", "SpanNearQuery",
            "NestedQuery",
        ]
        for export in expected_exports:
            assert export in query_module.__all__, f"{export}이(가) __all__에 없습니다"

    def test_imported_classes_are_functional(self):
        """import한 모든 클래스가 실제로 동작하는지 확인합니다."""
        from elastic_query_builder.query import (
            TermQuery, MatchQuery, MatchAllQuery,
            BoolQueryBuilder, DisMaxQuery,
            SpanTermQuery, SpanNearQuery,
            NestedQuery,
        )

        assert "term" in TermQuery.build("f", "v")
        assert "match" in MatchQuery.build("f", "v")
        assert "match_all" in MatchAllQuery.build()
        assert "bool" in BoolQueryBuilder().build()
        assert "dis_max" in DisMaxQuery.build(queries=[{"match_all": {}}])
        assert "span_term" in SpanTermQuery.build("f", "v")
        assert "span_near" in SpanNearQuery.build(
            clauses=[{"span_term": {"f": "v"}}], slop=1
        )
        assert "nested" in NestedQuery.build("path", {"match_all": {}})
