"""query/leaf/__init__.py에 대한 단위 테스트.

리프 쿼리 패키지에서 모든 클래스를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestLeafQueryImports:
    """리프 쿼리 패키지 import 테스트."""

    def test_import_term_query(self):
        """query.leaf 패키지에서 TermQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import TermQuery
        assert TermQuery is not None

    def test_import_terms_query(self):
        """query.leaf 패키지에서 TermsQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import TermsQuery
        assert TermsQuery is not None

    def test_import_match_query(self):
        """query.leaf 패키지에서 MatchQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import MatchQuery
        assert MatchQuery is not None

    def test_import_match_phrase_query(self):
        """query.leaf 패키지에서 MatchPhraseQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import MatchPhraseQuery
        assert MatchPhraseQuery is not None

    def test_import_range_query(self):
        """query.leaf 패키지에서 RangeQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import RangeQuery
        assert RangeQuery is not None

    def test_import_wildcard_query(self):
        """query.leaf 패키지에서 WildcardQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import WildcardQuery
        assert WildcardQuery is not None

    def test_import_exists_query(self):
        """query.leaf 패키지에서 ExistsQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import ExistsQuery
        assert ExistsQuery is not None

    def test_import_ids_query(self):
        """query.leaf 패키지에서 IdsQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import IdsQuery
        assert IdsQuery is not None

    def test_import_match_all_query(self):
        """query.leaf 패키지에서 MatchAllQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import MatchAllQuery
        assert MatchAllQuery is not None

    def test_import_match_none_query(self):
        """query.leaf 패키지에서 MatchNoneQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.leaf import MatchNoneQuery
        assert MatchNoneQuery is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 모든 클래스를 포함하는지 확인합니다."""
        import elastic_query_builder.query.leaf as leaf_module
        expected_exports = [
            "TermQuery", "TermsQuery",
            "MatchQuery", "MatchPhraseQuery",
            "RangeQuery",
            "WildcardQuery",
            "ExistsQuery",
            "IdsQuery",
            "MatchAllQuery", "MatchNoneQuery",
        ]
        for export in expected_exports:
            assert export in leaf_module.__all__, f"{export}이(가) __all__에 없습니다"

    def test_imported_classes_are_functional(self):
        """import한 클래스들이 실제로 동작하는지 확인합니다."""
        from elastic_query_builder.query.leaf import (
            TermQuery, MatchQuery, RangeQuery, ExistsQuery,
            IdsQuery, MatchAllQuery, MatchNoneQuery,
        )

        # 각 클래스가 쿼리를 생성할 수 있는지 간단히 확인
        assert "term" in TermQuery.build("f", "v")
        assert "match" in MatchQuery.build("f", "v")
        assert "range" in RangeQuery.build("f", gte=1)
        assert "exists" in ExistsQuery.build("f")
        assert "ids" in IdsQuery.build(["1"])
        assert "match_all" in MatchAllQuery.build()
        assert "match_none" in MatchNoneQuery.build()
