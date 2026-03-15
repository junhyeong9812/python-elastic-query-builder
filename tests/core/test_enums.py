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

class TestSortMissing:
    """SortMissing 열거형 테스트."""

    def test_first_value(self):
        """FIRST의 값이 '_first'인지 확인합니다."""
        assert SortMissing.FIRST.value == "_first"

    def test_last_value(self):
        """LAST의 값이 '_last'인지 확인합니다."""
        assert SortMissing.LAST.value == "_last"

    def test_is_string_enum(self):
        """SortMissing이 str 열거형이어서 문자열로 직접 사용 가능한지 확인합니다."""
        assert isinstance(SortMissing.FIRST, str)
        assert SortMissing.FIRST == "_first"
        assert SortMissing.LAST == "_last"

    def test_member_count(self):
        """SortMissing에 정확히 2개의 멤버가 있는지 확인합니다."""
        assert len(SortMissing) == 2

class TestBoolClause:
    """BoolClause 열거형 테스트."""

    def test_must_value(self):
        """MUST의 값이 'must'인지 확인합니다."""
        assert BoolClause.MUST.value == "must"

    def test_should_value(self):
        """SHOULD의 값이 'should'인지 확인합니다."""
        assert BoolClause.SHOULD.value == "should"

    def test_must_not_value(self):
        """MUST_NOT의 값이 'must_not'인지 확인합니다."""
        assert BoolClause.MUST_NOT.value == "must_not"

    def test_filter_value(self):
        """FILTER의 값이 'filter'인지 확인합니다."""
        assert BoolClause.FILTER.value == "filter"

    def test_is_string_enum(self):
        """BoolClause가 str 열거형이어서 문자열로 직접 사용 가능한지 확인합니다."""
        assert isinstance(BoolClause.MUST, str)
        assert BoolClause.MUST == "must"
        assert BoolClause.SHOULD == "should"
        assert BoolClause.MUST_NOT == "must_not"
        assert BoolClause.FILTER == "filter"

    def test_can_use_as_dict_key(self):
        """딕셔너리 키로 사용할 때 문자열 키와 동일하게 동작하는지 확인합니다."""
        query = {BoolClause.MUST: []}
        assert "must" in query

    def test_member_count(self):
        """BoolClause에 정확히 4개의 멤버가 있는지 확인합니다."""
        assert len(BoolClause) == 4