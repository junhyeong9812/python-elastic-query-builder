import pytest
from elastic_query_builder.core.enums import SortOrder, SortMissing, BoolClause

"""core/enums.py에 대한 단위 테스트.

SortOrder, SortMissing, BoolClause 열거형이 올바른 값을 가지는지,
그리고 str 열거형으로서 문자열처럼 사용할 수 있는지 검증합니다.
"""

class TestSortOrder:
    """SortOrder 열거형 테스트."""

    def test_asc_value(self):
        """ASC의 값이 'asc'인지 확인합니다."""
        assert SortOrder.ASC.value == "asc"

    def test_desc_value(self):
        """DESC의 값이 'desc'인지 확인합니다."""
        assert SortOrder.DESC.value == "desc"

    def test_is_string_enum(self):
        """SortOrder가 str 열거형이어서 문자열로 직접 사용 가능한지 확인합니다."""
        assert isinstance(SortOrder.ASC, str)
        assert SortOrder.ASC == "asc"
        assert SortOrder.DESC == "desc"

    def test_can_use_in_dict_value(self):
        """딕셔너리 값으로 사용할 때 문자열처럼 동작하는지 확인합니다."""
        sort_config = {"order": SortOrder.ASC}
        assert sort_config["order"] == "asc"

    def test_member_count(self):
        """SortOrder에 정확히 2개의 멤버가 있는지 확인합니다."""
        assert len(SortOrder) == 2