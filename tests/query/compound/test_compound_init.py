"""query/compound/__init__.py에 대한 단위 테스트.

복합 쿼리 패키지에서 모든 클래스를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestCompoundQueryImports:
    """복합 쿼리 패키지 import 테스트."""

    def test_import_bool_query_builder(self):
        """query.compound 패키지에서 BoolQueryBuilder를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.compound import BoolQueryBuilder
        assert BoolQueryBuilder is not None

    def test_import_dis_max_query(self):
        """query.compound 패키지에서 DisMaxQuery를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.query.compound import DisMaxQuery
        assert DisMaxQuery is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 모든 클래스를 포함하는지 확인합니다."""
        import elastic_query_builder.query.compound as compound_module
        expected_exports = ["BoolQueryBuilder", "DisMaxQuery"]
        for export in expected_exports:
            assert export in compound_module.__all__, f"{export}이(가) __all__에 없습니다"

    def test_imported_classes_are_functional(self):
        """import한 클래스들이 실제로 동작하는지 확인합니다."""
        from elastic_query_builder.query.compound import BoolQueryBuilder, DisMaxQuery

        # BoolQueryBuilder가 쿼리를 생성할 수 있는지 확인
        bool_result = BoolQueryBuilder().build()
        assert "bool" in bool_result

        # DisMaxQuery가 쿼리를 생성할 수 있는지 확인
        dis_max_result = DisMaxQuery.build(queries=[{"match_all": {}}])
        assert "dis_max" in dis_max_result
