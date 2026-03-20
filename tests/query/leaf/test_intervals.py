"""IntervalsQuery 테스트."""

from elastic_query_builder.query.leaf.intervals import IntervalsQuery


class TestIntervalsQuery:
    """IntervalsQuery.build 메서드 테스트."""

    def test_basic_match_rule(self):
        """기본 match 규칙으로 intervals 쿼리를 생성한다."""
        result = IntervalsQuery.build("my_text", {"match": {"query": "hot water"}})
        assert result == {
            "intervals": {
                "my_text": {"match": {"query": "hot water"}}
            }
        }

    def test_all_of_rule(self):
        """all_of 규칙으로 intervals 쿼리를 생성한다."""
        rule = {
            "all_of": {
                "intervals": [
                    {"match": {"query": "hot"}},
                    {"match": {"query": "dog"}},
                ]
            }
        }
        result = IntervalsQuery.build("my_text", rule)
        assert result == {"intervals": {"my_text": rule}}

    def test_any_of_rule(self):
        """any_of 규칙으로 intervals 쿼리를 생성한다."""
        rule = {
            "any_of": {
                "intervals": [
                    {"match": {"query": "hot dog"}},
                    {"match": {"query": "hot water"}},
                ]
            }
        }
        result = IntervalsQuery.build("my_text", rule)
        assert result == {"intervals": {"my_text": rule}}

    def test_with_ordered_and_max_gaps(self):
        """ordered와 max_gaps 옵션을 포함한 all_of 규칙으로 intervals 쿼리를 생성한다."""
        rule = {
            "all_of": {
                "ordered": True,
                "max_gaps": 0,
                "intervals": [
                    {"match": {"query": "hot"}},
                    {"match": {"query": "dog"}},
                ],
            }
        }
        result = IntervalsQuery.build("my_text", rule)
        assert result == {"intervals": {"my_text": rule}}

    def test_nested_rules(self):
        """중첩된 규칙으로 intervals 쿼리를 생성한다."""
        rule = {
            "all_of": {
                "ordered": True,
                "intervals": [
                    {
                        "any_of": {
                            "intervals": [
                                {"match": {"query": "hot"}},
                                {"match": {"query": "warm"}},
                            ]
                        }
                    },
                    {"match": {"query": "dog"}},
                ],
            }
        }
        result = IntervalsQuery.build("my_text", rule)
        assert result == {"intervals": {"my_text": rule}}
