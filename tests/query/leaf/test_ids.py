"""query/leaf/ids.py에 대한 단위 테스트.

IdsQuery가 올바른 Elasticsearch ids 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.ids import IdsQuery


class TestIdsQuery:
    """IdsQuery 테스트."""

    def test_ids_query(self):
        """기본 IDs 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = IdsQuery.build(["1", "2", "3"])
        expected = {"ids": {"values": ["1", "2", "3"]}}
        assert result == expected

    def test_ids_query_single_id(self):
        """단일 ID로 IDs 쿼리를 생성할 수 있는지 확인합니다."""
        result = IdsQuery.build(["42"])
        expected = {"ids": {"values": ["42"]}}
        assert result == expected

    def test_ids_query_empty_list(self):
        """빈 리스트로 IDs 쿼리를 생성할 수 있는지 확인합니다."""
        result = IdsQuery.build([])
        expected = {"ids": {"values": []}}
        assert result == expected

    def test_ids_query_structure(self):
        """IDs 쿼리 결과의 구조가 올바른지 확인합니다."""
        result = IdsQuery.build(["a", "b"])
        assert "ids" in result
        assert "values" in result["ids"]
        assert isinstance(result["ids"]["values"], list)

    def test_ids_query_preserves_order(self):
        """IDs 쿼리가 입력된 ID의 순서를 유지하는지 확인합니다."""
        ids = ["3", "1", "2"]
        result = IdsQuery.build(ids)
        assert result["ids"]["values"] == ["3", "1", "2"]
