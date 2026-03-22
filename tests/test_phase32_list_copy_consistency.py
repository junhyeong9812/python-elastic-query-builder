"""Phase 32 테스트 — 리스트 복사 비일관성 수정 검증.

set_search_after, set_fields, set_stored_fields에 전달한 list를
외부에서 수정해도 빌더 내부 상태가 오염되지 않음을 확인합니다.
"""

import pytest
from elastic_query_builder import QueryBuilder


class TestSetSearchAfterListCopy:
    """set_search_after: 외부 list 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        values = [1234567890, "doc_id_1"]
        builder = QueryBuilder().set_search_after(values)

        values.append("extra")
        values[0] = 9999

        result = builder.build()
        assert result["search_after"] == [1234567890, "doc_id_1"]

    def test_list_identity_is_different(self):
        values = [100, "abc"]
        builder = QueryBuilder().set_search_after(values)

        result = builder.build()
        assert result["search_after"] is not values


class TestSetFieldsListCopy:
    """set_fields: 외부 list 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        fields = ["title", "description"]
        builder = QueryBuilder().set_fields(fields)

        fields.append("extra_field")
        fields[0] = "modified"

        result = builder.build()
        assert result["fields"] == ["title", "description"]


class TestSetStoredFieldsListCopy:
    """set_stored_fields: 외부 list 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        fields = ["title", "body"]
        builder = QueryBuilder().set_stored_fields(fields)

        fields.append("extra")
        fields[0] = "modified"

        result = builder.build()
        assert result["stored_fields"] == ["title", "body"]
