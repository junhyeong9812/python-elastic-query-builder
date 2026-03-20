"""elastic_query_builder/__init__.py에 대한 단위 테스트.

패키지 최상위에서 주요 클래스를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestPackageTopLevelImports:
    """패키지 최상위 import 테스트."""

    def test_import_query_builder(self):
        """최상위 패키지에서 QueryBuilder를 import할 수 있는지 확인합니다."""
        from elastic_query_builder import QueryBuilder
        assert QueryBuilder is not None

    def test_import_sort_order(self):
        """최상위 패키지에서 SortOrder를 import할 수 있는지 확인합니다."""
        from elastic_query_builder import SortOrder
        assert SortOrder is not None

    def test_import_sort_missing(self):
        """최상위 패키지에서 SortMissing을 import할 수 있는지 확인합니다."""
        from elastic_query_builder import SortMissing
        assert SortMissing is not None

    def test_import_bool_clause(self):
        """최상위 패키지에서 BoolClause를 import할 수 있는지 확인합니다."""
        from elastic_query_builder import BoolClause
        assert BoolClause is not None

    def test_import_bool_query_builder(self):
        """최상위 패키지에서 BoolQueryBuilder를 import할 수 있는지 확인합니다."""
        from elastic_query_builder import BoolQueryBuilder
        assert BoolQueryBuilder is not None

    def test_import_aggregation_builder(self):
        """최상위 패키지에서 AggregationBuilder를 import할 수 있는지 확인합니다."""
        from elastic_query_builder import AggregationBuilder
        assert AggregationBuilder is not None

    def test_import_sort_builder(self):
        """최상위 패키지에서 SortBuilder를 import할 수 있는지 확인합니다."""
        from elastic_query_builder import SortBuilder
        assert SortBuilder is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 모든 주요 클래스를 포함하는지 확인합니다."""
        import elastic_query_builder as pkg
        expected_exports = [
            "QueryBuilder",
            "SortOrder", "SortMissing", "BoolClause",
            "BoolQueryBuilder", "AggregationBuilder", "SortBuilder",
        ]
        for export in expected_exports:
            assert export in pkg.__all__, f"{export}이(가) __all__에 없습니다"

    def test_query_builder_is_functional(self):
        """import한 QueryBuilder가 실제로 동작하는지 확인합니다."""
        from elastic_query_builder import QueryBuilder, SortOrder
        result = (
            QueryBuilder()
            .set_match_all()
            .set_size(10)
            .add_sort("date", SortOrder.DESC)
            .build()
        )
        assert result["query"] == {"match_all": {}}
        assert result["size"] == 10
        assert "sort" in result

    def test_enums_are_functional(self):
        """import한 열거형들이 실제로 동작하는지 확인합니다."""
        from elastic_query_builder import SortOrder, SortMissing, BoolClause
        assert SortOrder.ASC.value == "asc"
        assert SortMissing.LAST.value == "_last"
        assert BoolClause.MUST.value == "must"
