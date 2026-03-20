"""sort/__init__.py에 대한 단위 테스트.

Sort 패키지에서 SortBuilder를 올바르게 import할 수 있는지 검증합니다.
"""

import pytest


class TestSortPackageImports:
    """Sort 패키지 import 테스트."""

    def test_import_sort_builder(self):
        """sort 패키지에서 SortBuilder를 import할 수 있는지 확인합니다."""
        from elastic_query_builder.sort import SortBuilder
        assert SortBuilder is not None

    def test_all_exports_defined(self):
        """__all__이 정의되어 있고 SortBuilder를 포함하는지 확인합니다."""
        import elastic_query_builder.sort as sort_module
        assert "SortBuilder" in sort_module.__all__

    def test_imported_sort_builder_is_functional(self):
        """import한 SortBuilder가 실제로 동작하는지 확인합니다."""
        from elastic_query_builder.sort import SortBuilder
        builder = SortBuilder()
        assert builder.is_empty() is True
        builder.add("field")
        assert builder.is_empty() is False
        result = builder.build()
        assert result == [{"field": {}}]
